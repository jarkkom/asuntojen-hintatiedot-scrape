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
        <td class="cellAlignRight">64,75</td>
        <td class="cellAlignRight">450800,1</td>
        <td class="cellAlignRight">7044,2</td>
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
        <td class="cellAlignRight">68,12</td>
        <td class="cellAlignRight">455000,23</td>
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
                "m2": 64.75,
                "price": 450800.1,
                "price_per_m2": 7044.2,
                "year": 2012,
                "floor": "4/5",
                "elevator": "on",
                "condition": "hyvä",
                "lot": "oma",
                "energy_class": "D2013",
                "id": "953ca2e81f42a8afcab135105408f7a8",
            },
            {
                "district": "Länsi-pasila",
                "description": "3h+k+kph+s+vh+t...",
                "building_type": "kt",
                "m2": 68.12,
                "price": 455000.23,
                "price_per_m2": 6691,
                "year": 2012,
                "floor": "1/5",
                "elevator": "on",
                "condition": "hyvä",
                "lot": "oma",
                "energy_class": "D2013",
                "id": "0a8493061855d350d8aba0726ccc07cd",
            },
        ]

        self.maxDiff = None
        self.assertEqual(
            api.parse_page(html),
            (expected_sales, 0),
        )

    @patch("api.logging")
    def test_parse_page_next_page(self, mock_logging):
        html = """
<html><body><table><tbody>
    <tr>
        <td class="more">
            <form action="" method="get">
            <input type="hidden" name="c" value="Helsinki">
            <input type="hidden" name="cr" value="1">
            <input type="hidden" name="t" value="3">
            <input type="hidden" name="l" value="0">
            <input type="hidden" name="z" value="1">
            <input type="hidden" name="search" value="1">
            <input type="hidden" name="sf" value="0">
            <input type="hidden" name="so" value="a">
            <input type="hidden" name="renderType" value="renderTypeTable">
            <input type="hidden" name="print" value="0">
            <input type="submit" class="submit" name="submit" value="« edellinen sivu">
            </form>
        </td>
        <td align="center">2</td>
        <td class="more" align="right">
            <form action="" method="get">
            <input type="hidden" name="c" value="Helsinki">
            <input type="hidden" name="cr" value="1">
            <input type="hidden" name="t" value="3">
            <input type="hidden" name="l" value="0">
            <input type="hidden" name="z" value="3">
            <input type="hidden" name="search" value="1">
            <input type="hidden" name="sf" value="0">
            <input type="hidden" name="so" value="a">
            <input type="hidden" name="renderType" value="renderTypeTable">
            <input type="hidden" name="print" value="0">
            <input type="submit" class="submit" name="submit" value="seuraava sivu »">
            </form>
        </td>
    </tr>
</tbody></table></body></html>
"""

        (_, actualNextPage) = api.parse_page(html)
        self.assertEqual(3, actualNextPage)


    @patch("api.logging")
    def test_parse_page_next_page_not_found(self, mock_logging):
        html = "<html><body><table><tbody></tbody></table></body></html>"

        (_, actualNextPage) = api.parse_page(html)
        self.assertEqual(0, actualNextPage)


if __name__ == "__main__":
    unittest.main()
