# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

wallet_cli = typer.Typer(
    name="wallet", help="Manage your wallets in Zetta AI Network.", no_args_is_help=True
)


@wallet_cli.command(name="create", help="Create a new wallet for current user.")
@synchronizer.create_blocking
async def create(json: bool = False):
    pass


@wallet_cli.command(name="import", help="Import a new wallet for current user.")
@synchronizer.create_blocking
async def import_wallet(json: bool = False):
    pass


@wallet_cli.command(name="unbind", help="Unbind a wallet for current user.")
@synchronizer.create_blocking
async def unbind(json: bool = False):
    pass


@wallet_cli.command(name="balance", help="get balance for the current wallet")
@synchronizer.create_blocking
async def balance(json: bool = False):
    pass
