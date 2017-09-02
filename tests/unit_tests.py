import unittest
import os
import sys
import mock
from xkcd_dl.cli import update_dict, download_all, download_xkcd_range, is_valid_comic, download_one
import xkcd_dl.cli
import json
import tempfile
from io import StringIO
from requests import Response
from requests.packages.urllib3.response import HTTPResponse
from mock import MagicMock
import shutil



def get_fake_xkcd_json_dict():
    from tests.inputs import XKCD_ARCHIVE_JSON
    return json.loads(XKCD_ARCHIVE_JSON)


def get_info_data():
    from tests.inputs import INFO_URL_DATA
    return INFO_URL_DATA


def get_comic_info():
    from tests.inputs import VALID_COMIC_INFO
    return VALID_COMIC_INFO


class Unittests(unittest.TestCase):
    def setUp(self):
        sys.stdout = StringIO()

    @mock.patch('xkcd_dl.cli.requests.get')
    def test_update_dict(self, mock_api_call):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        xkcd_dl.cli.xkcd_dict_location = tmp_file.name
        from tests.inputs import ARCHIVE_URL_CONTENT
        res = ARCHIVE_URL_CONTENT

        mock_api_call.return_value.status_code = 200
        mock_api_call.return_value.content = res

        update_dict()
        
        with open(tmp_file.name) as json_file:
            data = json.load(json_file)
        assert len(data) == 1849
        os.remove(tmp_file.name)

    @mock.patch('xkcd_dl.cli.read_dict', side_effect=get_fake_xkcd_json_dict)
    @mock.patch('xkcd_dl.cli.download_one')
    def test_download_all(self, download_one_stub, fake_dict):
        download_all()
        assert download_one_stub.call_count == 21

    @mock.patch('xkcd_dl.cli.is_valid_comic', return_value=True)
    @mock.patch('xkcd_dl.cli.read_dict', side_effect=get_fake_xkcd_json_dict)
    @mock.patch('xkcd_dl.cli.download_one')
    def test_download_xkcd_range_normal(self, download_one_stub, fake_dict, is_valid_comic_stub):
        download_xkcd_range(233, 236)
        assert download_one_stub.call_count == 4

    @mock.patch('xkcd_dl.cli.is_valid_comic', return_value=True)
    @mock.patch('xkcd_dl.cli.read_dict', side_effect=get_fake_xkcd_json_dict)
    @mock.patch('xkcd_dl.cli.download_one')
    def test_download_xkcd_range_with_404(self, download_one_stub, fake_dict, is_valid_comic_stub):
        download_xkcd_range(400, 405)
        assert download_one_stub.call_count == 5

    @mock.patch('xkcd_dl.cli.read_dict', side_effect=get_fake_xkcd_json_dict)
    @mock.patch('xkcd_dl.cli.download_one')
    def test_download_xkcd_range_wrong_range(self, download_one_stub, fake_dict):
        download_xkcd_range(405, 400)
        assert sys.stdout.getvalue().strip() == "Start must be smaller than End."

    @mock.patch('xkcd_dl.cli.requests.get')
    def test_valid_comic(self, mock_api_call):
        from tests.inputs import INFO_URL_DATA
        res = INFO_URL_DATA
        mock_api_call.return_value.status_code = 200
        mock_api_call.return_value.json.return_value = res
        assert is_valid_comic(100) == True

    @mock.patch('xkcd_dl.cli.requests.get')
    def test_invalid_comic(self, mock_api_call):
        from tests.inputs import INFO_URL_DATA
        res = INFO_URL_DATA
        mock_api_call.return_value.status_code = 200
        mock_api_call.return_value.json.return_value = res
        assert is_valid_comic(9999999999999999) == False

    @mock.patch('xkcd_dl.cli.shutil.copyfileobj')
    @mock.patch('xkcd_dl.cli.requests.get')
    def test_download_one(self, mock_call, fake_copyfileobj):
        from tests.inputs import VALID_COMIC_INFO
        from tests.inputs import IMAGE_PAGE_CONTENT_1550
        comic_info = VALID_COMIC_INFO
        page_info = IMAGE_PAGE_CONTENT_1550

        mock_info_call = MagicMock(spec=Response)
        mock_info_call.json.return_value = get_comic_info()
        mock_info_call.return_value.status_code = 200
        mock_info_call.return_value = page_info

        mock_image_call = MagicMock(spec=Response)
        mock_image_call.status_code = 200
        mock_image_call.return_value.json.return_value = comic_info
        mock_image_call.content = page_info

        mock_image_content_call = MagicMock(spec=Response)
        mock_image_content_call.raw = MagicMock(spec=HTTPResponse)
        mock_image_content_call.status_code = 200

        mock_call.side_effect = [mock_info_call, mock_image_call, mock_image_content_call]
        xkcd_dl.cli.WORKING_DIRECTORY = tempfile.mkdtemp()
        download_one(get_fake_xkcd_json_dict(), 1550)
        xkcd_download_folder = xkcd_dl.cli.WORKING_DIRECTORY + "/xkcd_archive/1550/"
        files = os.listdir(xkcd_download_folder)

        assert "description.txt" in files
        assert 'EpisodeVII.jpg' in files
        assert os.path.getsize(xkcd_download_folder + "description.txt") == 238

        shutil.rmtree(xkcd_dl.cli.WORKING_DIRECTORY, ignore_errors=True)

    @mock.patch('xkcd_dl.cli.shutil.copyfileobj')
    @mock.patch('xkcd_dl.cli.requests.get')
    def test_download_duplicate(self, mock_call, fake_copyfileobj):
        from tests.inputs import VALID_COMIC_INFO
        from tests.inputs import IMAGE_PAGE_CONTENT_1550
        comic_info = VALID_COMIC_INFO
        page_info = IMAGE_PAGE_CONTENT_1550

        mock_info_call = MagicMock(spec=Response)
        mock_info_call.json.return_value = get_comic_info()
        mock_info_call.return_value.status_code = 200
        mock_info_call.return_value = page_info

        mock_image_call = MagicMock(spec=Response)
        mock_image_call.status_code = 200
        mock_image_call.return_value.json.return_value = comic_info
        mock_image_call.content = page_info

        mock_image_content_call = MagicMock(spec=Response)
        mock_image_content_call.raw = MagicMock(spec=HTTPResponse)
        mock_image_content_call.status_code = 200

        mock_call.side_effect = [mock_info_call, mock_image_call, mock_image_content_call, mock_info_call,
                                 mock_image_call, mock_image_content_call]
        xkcd_dl.cli.WORKING_DIRECTORY = tempfile.mkdtemp()
        download_one(get_fake_xkcd_json_dict(), 1550)
        download_one(get_fake_xkcd_json_dict(), 1550)

        assert sys.stdout.getvalue().split('\n')[-2] == "xkcd  number '1550' has already been downloaded!"

        shutil.rmtree(xkcd_dl.cli.WORKING_DIRECTORY, ignore_errors=True)

    @mock.patch('xkcd_dl.cli.requests.get')
    def test_download_one_invalid(self, mock_api_call):
        download_one(get_fake_xkcd_json_dict(), 11)
        assert sys.stdout.getvalue().strip() == "11 does not exist! Please try with a different option"

    @mock.patch('xkcd_dl.cli.requests.get')
    def test_download_exclusion_list(self, mock_api_call):
        download_one(get_fake_xkcd_json_dict(), 1525)
        assert "1525 is special. It does not have an image." in sys.stdout.getvalue()
