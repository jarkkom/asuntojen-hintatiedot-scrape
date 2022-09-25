import api
import unittest
from unittest.mock import patch, MagicMock, sentinel


class TestFetchPage(unittest.TestCase):
    @patch("api.logging")
    @patch("api.requests")
    def test_fetch_page_ok(self, mock_requests, mock_logging):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = sentinel.response_text

        mock_requests.get.return_value = mock_response

        expected_params = {
            "c": "Helsinki",
            "cr": "1",
            "h": "1",
            "r": 4,
            "amin": "100.0",
            "amax": "",
            "sf": 0,
            "so": "a",
            "search": 1,
            "renderType": "renderTypeTable",
            "print": "0",
            "z": 1,
        }

        self.assertEqual(
            api.fetch_page(1),
            sentinel.response_text,
        )
        mock_requests.get.assert_called_once_with(
            "https://asuntojen.hintatiedot.fi/haku/",
            params=expected_params,
        )
        mock_logging.info.assert_called_once()

    @patch("api.logging")
    @patch("api.requests")
    def test_fetch_page_fail(self, mock_requests, mock_logging):
        mock_response = MagicMock()
        mock_response.status_code = 400

        mock_requests.get.return_value = mock_response

        self.assertIsNone(api.fetch_page(1))
        mock_logging.error.assert_called_once()


class TestParsePage(unittest.TestCase):
    @patch("api.logging")
    def test_parse_page_sales_ok(self, mock_logging):
        html = """
<html><body><table>
    <tr class="">
        <td class="neighborhood">Pasila</td>
        <td class="">3h +k +s</td>
        <td class="houseType">kt</td>
        <td class="cellAlignRight">64,00</td>
        <td class="cellAlignRight">450800</td>
        <td class="cellAlignRight">7044</td>
        <td class="cellAlignRight">2012</td>
        <td class="">4/5</td>
        <td class="">on</td>
        <td class="">hyvä</td>
        <td class="">oma							</td><td class="">D<sub>2013</sub></td>
    </tr>
    <tr class="">
        <td class="neighborhood">Länsi-pasila</td>
        <td class="">3h+k+kph+s+vh+t...</td>
        <td class="houseType">kt</td>
        <td class="cellAlignRight">68,00</td>
        <td class="cellAlignRight">455000</td>
        <td class="cellAlignRight">6691</td>
        <td class="cellAlignRight">2012</td>
        <td class="">1/5</td>
        <td class="">on</td>
        <td class="">hyvä</td>
        <td class="">oma							</td><td class="">D<sub>2013</sub></td>
    </tr>                        
</table></body></html>
"""

        expected_sales = [
            {
                "district": "Pasila",
                "description": "3h +k +s",
                "building_type": "kt",
                "m2": "64,00",
                "price": "450800",
                "price_per_m2": "7044",
                "year": "2012",
                "floor": "4/5",
                "elevator": "on",
                "condition": "hyvä",
                "lot": "oma",
                "energy_class": "D2013",
                "id": "dbeb0e4216f60c37b5ec4a68a461ba0b",
            },
            {
                "district": "Länsi-pasila",
                "description": "3h+k+kph+s+vh+t...",
                "building_type": "kt",
                "m2": "68,00",
                "price": "455000",
                "price_per_m2": "6691",
                "year": "2012",
                "floor": "1/5",
                "elevator": "on",
                "condition": "hyvä",
                "lot": "oma",
                "energy_class": "D2013",
                "id": "920aa6a098f7123c73ff5bc369631f4a",
            },
        ]

        self.maxDiff = None
        self.assertEqual(
            api.parse_page(html),
            (expected_sales, 0),
        )


if __name__ == "__main__":
    unittest.main()
