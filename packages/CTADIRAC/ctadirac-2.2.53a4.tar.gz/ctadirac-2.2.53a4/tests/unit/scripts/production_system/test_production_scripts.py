from unittest.mock import patch
import pytest
from typer.testing import CliRunner
from CTADIRAC.Core.Utilities.typer_callbacks import PRODUCTION_FIELDS
from CTADIRAC.ProductionSystem.scripts.cta_prod_get_all import (
    extract_user_name_from_dn,
    fill_columns,
    app,
)
from tests.unit.production import PRODUCTION_RESULTS

runner = CliRunner()


def test_extract_user_name_from_dn():
    name = "Surname Lastname"
    dn = f"/O=GRID-FR/C=FR/O=CNRS/OU=LUPM/CN={name}"
    result = extract_user_name_from_dn(dn)
    assert result == name


def test_fill_columns():
    result = fill_columns(PRODUCTION_RESULTS[0], PRODUCTION_FIELDS, True)
    assert isinstance(result, list)


@pytest.fixture
def mock_production_client():
    with patch(
        "DIRAC.ProductionSystem.Client.ProductionClient.ProductionClient"
    ) as mock_client:
        yield mock_client


def test_main(mock_production_client):
    mock_client_instance = mock_production_client.return_value
    mock_client_instance.getProductions.return_value = {
        "OK": True,
        "Value": PRODUCTION_RESULTS,
    }

    result = runner.invoke(app, ["--long", "--cond", '{"Status": "Active"}'])
    assert result.exit_code == 0
    mock_client_instance.getProductions.assert_called_once_with(
        condDict={"Status": "Active"}
    )
    assert PRODUCTION_RESULTS[0]["AuthorGroup"] in result.stdout
