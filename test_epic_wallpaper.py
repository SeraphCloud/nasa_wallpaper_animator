import os
import pytest
from unittest.mock import patch, MagicMock
from epic_wallpaper import NASAWallpaperDownloader, WallpaperAnimator


class TestNASAWallpaperDownloader:
    def test_init_creates_cache_dir(self, tmp_path):
        cache_dir = tmp_path / "test_cache"
        downloader = NASAWallpaperDownloader(cache_dir=str(cache_dir))
        assert cache_dir.exists()

    def test_clear_cache(self, tmp_path):
        downloader = NASAWallpaperDownloader(cache_dir=str(tmp_path))
        # Create fake jpg files
        (tmp_path / "00.jpg").write_text("fake image")
        (tmp_path / "01.jpg").write_text("fake image")
        (tmp_path / "not_jpg.txt").write_text("not jpg")

        downloader.clear_cache()

        # Only jpg files should be deleted
        remaining = list(tmp_path.glob("*"))
        assert len(remaining) == 1
        assert remaining[0].name == "not_jpg.txt"

    @patch('requests.get')
    def test_download_sequence_success(self, mock_get, tmp_path):
        downloader = NASAWallpaperDownloader(cache_dir=str(tmp_path))

        # Mock API response
        api_mock = MagicMock()
        api_mock.status_code = 200
        api_mock.json.return_value = [
            {"image": "test_image1"},
            {"image": "test_image2"}
        ]

        # Mock image download response
        img_mock = MagicMock()
        img_mock.content = b"fake image data"

        # Side effect to return different mocks
        mock_get.side_effect = [api_mock, img_mock, img_mock]

        result = downloader.download_sequence("2024-12-07")

        assert len(result) == 2
        assert all(os.path.exists(path) for path in result)
        assert mock_get.call_count == 3  # 1 API + 2 images

    @patch('requests.get')
    def test_download_sequence_api_error(self, mock_get):
        downloader = NASAWallpaperDownloader()

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = downloader.download_sequence("2024-12-07")

        assert result == []

    @patch('requests.get')
    def test_download_sequence_no_images(self, mock_get):
        downloader = NASAWallpaperDownloader()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        result = downloader.download_sequence("2024-12-07")

        assert result == []


class TestWallpaperAnimator:
    def test_init(self):
        animator = WallpaperAnimator(fps=1.0)
        assert animator.fps == 1.0

    def test_init_default_fps(self):
        animator = WallpaperAnimator()
        assert animator.fps == 0.5

    # Note: animate() runs an infinite loop, so testing it directly is tricky
    # In a real scenario, you might mock time.sleep and ctypes, but for now, skip