#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import re
from rich import print
from rich.console import Console
from rich.table import Table
import tempfile
import typer

import click
import prettytable
import toml

from snowcli import config, utils
from snowcli.config import AppConfig
from snowcli.snowsql_config import SnowsqlConfig

console = Console()
app = typer.Typer()
EnvironmentOption = typer.Option("dev", help='Environment name')

def print_db_cursor(cursor):
    if cursor.description:
        table = Table(*[col[0] for col in cursor.description])
        for row in cursor.fetchall():
            table.add_row(*[str(c) for c in row])
        print(table)

@app.command("list")
def streamlit_list(environment: str = EnvironmentOption):
    """
    List streamlit apps.
    """
    env_conf = AppConfig().config.get(environment)

    if config.isAuth():
        config.connectToSnowflake()
        results = config.snowflake_connection.listStreamlits(
            database=env_conf.get('database'),
            schema=env_conf.get('schema'),
            role=env_conf.get('role'),
            warehouse=env_conf.get('warehouse'))
        print_db_cursor(results)

@app.command("create")
def streamlit_create(environment: str = EnvironmentOption,
                     name: str = typer.Argument(..., help='Name of streamlit to be created.'),
                     file: Path = typer.Option('streamlit_app.py', 
                                               exists=True,
                                               readable=True,
                                               file_okay=True,
                                               help='Path to streamlit file')):
    """
    Create a streamlit app named NAME.
    """
    env_conf = AppConfig().config.get(environment)

    if config.isAuth():
        config.connectToSnowflake()
        results = config.snowflake_connection.createStreamlit(
            database=env_conf.get('database'),
            schema=env_conf.get('schema'),
            role=env_conf.get('role'),
            warehouse=env_conf.get('warehouse'),
            name=name,
            file=str(file))
        print_db_cursor(results)

@app.command("deploy")
def streamlit_deploy(environment: str = EnvironmentOption,
                     name: str = typer.Argument(..., help='Name of streamlit to be deployed.'),
                     file: Path = typer.Option('streamlit_app.py', 
                                               exists=True,
                                               readable=True,
                                               file_okay=True,
                                               help='Path to streamlit file'),
                     open_: bool = typer.Option(False, "--open", "-o", help='Open streamlit in browser.')):
    """
    Deploy streamlit with NAME.
    """
    env_conf = AppConfig().config.get(environment)

    if config.isAuth():
        config.connectToSnowflake()
        results = config.snowflake_connection.deployStreamlit(
            name=name, file_path=str(file), stage_path='/',
            role=env_conf.get('role'), overwrite=True)

        url = results.fetchone()[0]
        if open_:
            typer.launch(url)
        else:
            print(url)

typer_click_object = typer.main.get_command(app)
