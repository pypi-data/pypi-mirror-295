from ._version import __version__

import asyncio
import json
import os
import re
import traceback
from datetime import timedelta, datetime
from dateutil import tz
from dateutil.parser import isoparse
from urllib.parse import urljoin

import ipywidgets
import nbformat
import pandas as pd
from IPython.display import display, HTML

from seeq import spy
from seeq.sdk import ProjectsApi, AddOnsApi, SystemApi
from seeq.spy._datalab import is_datalab, is_ipython


class DataLabEnvMgr(ipywidgets.VBox):
    _local_base_path = "/home/datalab/.local/lib/"
    _global_base_path = "/seeq/python/global-packages/lib/"
    _system_base_path = "/usr/local/.pyenv/versions/"
    _global_base = "/seeq/python/global-packages"
    _categories = ["local", "global", "system"]
    _datalab_home = "/home/datalab"
    _version = __version__
    _full_width_table_css = """<style> #full-width-table { width: 100%; } </style>"""
    _datetime_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self):

        if not (is_datalab() and is_ipython()):
            super().__init__(children=[ipywidgets.HTML(value="This widget is only available in Data Lab.")])
            return

        self._markdown_doc = ipywidgets.HTML("""
        <h1>Data Lab Environment Manager</h1>
        <p>This tool helps Data Lab users transition their Notebooks between different Python versions,
        manage projects, and handle Python packages effectively.</p>
        <p>For detailed instructions, please refer to the 
        <a href="https://support.seeq.com/kb/latest/cloud/user-guide-data-lab-environment-manager"
        target="_blank">full documentation</a>.</p>
        """)

        self._config = self._generate_config()
        self._has_global_write_access = os.access(self._global_base_path, os.W_OK)
        self._user_timezone = tz.gettz(spy.utils.get_user_timezone(spy.session))

        # Projects Overview Section
        self._from_last_date_filter = ipywidgets.Dropdown(
            options=['Last 1 Month', 'Last 3 Months', 'Last 6 Months', 'Last 1 Year', 'All-time'],
            value='Last 6 Months',
            description='Last Used:',
            layout=ipywidgets.Layout(height="fit-content")
        )
        _scheduled_notebook_status = ["All", "Active", "Stopped", "None"]
        self._scheduled_notebook_filter = ipywidgets.Dropdown(
            options=_scheduled_notebook_status,
            value=_scheduled_notebook_status[0],
            style={'description_width': 'initial'},
            description='Scheduled Notebook:',
            layout=ipywidgets.Layout(height="fit-content")
        )
        _project_types = ["All"]
        self._project_type_filter = ipywidgets.Dropdown(
            options=_project_types,
            value=_project_types[0],
            description='Project Type:',
            layout=ipywidgets.Layout(height="fit-content")
        )
        self._sort_projects_by_filter = ipywidgets.Dropdown(
            options=["Last Updated", "Project Name"],
            value="Last Updated",
            description='Sort By:',
            layout=ipywidgets.Layout(height="fit-content")
        )
        self._project_report_output = ipywidgets.Output(
            layout=ipywidgets.Layout(overflow='auto', height='93%', padding='0px'))

        self._project_report_controls = ipywidgets.HBox(
            [self._from_last_date_filter, self._scheduled_notebook_filter, self._project_type_filter,
             self._sort_projects_by_filter],
            layout=ipywidgets.Layout(justify_content='space-between', height='7%', padding_left='10px',
                                     padding_right='10px'))
        self._project_report_progress_bar = ipywidgets.IntProgress(value=3, min=0, max=100,
                                                                   description='Loading Projects:',
                                                                   style={'description_width': 'initial'},
                                                                   layout=ipywidgets.Layout(width='auto'))

        self._project_report_wrap = ipywidgets.VBox([self._project_report_progress_bar],
                                                    layout=ipywidgets.Layout(overflow='auto', height='550px',
                                                                             padding='0px'))

        # Notebook Overview Section
        self._notebook_kernels_output = ipywidgets.Output(
            layout=ipywidgets.Layout(overflow='auto', height='auto', padding='0px', display="grid"))

        self._notebook_kernels_wrap = ipywidgets.VBox([self._notebook_kernels_output],
                                                      layout=ipywidgets.Layout(overflow='auto', height='550px',
                                                                               padding='0px'))

        # Packages Section
        self._packages_section_progress_bar = ipywidgets.IntProgress(value=3, min=0, max=100,
                                                                     description='Listing Packages:',
                                                                     style={'description_width': 'initial'},
                                                                     layout=ipywidgets.Layout(width='auto'))
        self._package_tabs = None

        package_scope_dropdown_options = ['local']
        if self._has_global_write_access:
            package_scope_dropdown_options.append('global')

        self._package_input = ipywidgets.Text(value='', placeholder='Enter package name', description='Install ',
                                              style={'description_width': 'initial'},
                                              layout=ipywidgets.Layout(height="fit-content"))

        self._package_version_dropdown = ipywidgets.Dropdown(options=[k for k, v in self._config.items()
                                                                      if v.get('pip_path') is not None],
                                                             description=' scope for Python ',
                                                             style={'description_width': 'initial'},
                                                             layout=ipywidgets.Layout(height="fit-content",
                                                                                      width="fit-content")
                                                             )

        self._package_scope_dropdown = ipywidgets.Dropdown(options=package_scope_dropdown_options,
                                                           value='local', description=' in ',
                                                           style={'description_width': 'initial'},
                                                           layout=ipywidgets.Layout(height="fit-content",
                                                                                    width="fit-content")
                                                           )

        self._package_install_button = ipywidgets.Button(description='Install', button_style='success')
        self._package_install_button.on_click(self._general_install_packages)

        self._package_install_box = ipywidgets.HBox([self._package_input,
                                                     self._package_scope_dropdown,
                                                     self._package_version_dropdown,
                                                     self._package_install_button],
                                                    layout=ipywidgets.Layout(justify_content='flex-start', height='7%'))

        self._packages_section_wrap = ipywidgets.VBox([self._packages_section_progress_bar],
                                                      layout=ipywidgets.Layout(overflow='auto', height='550px',
                                                                               padding='0px'))

        # Console Output Section
        self._console = ipywidgets.Output(layout=ipywidgets.Layout(overflow='auto', height='93%', padding='0px'))
        self._console_description = ipywidgets.Label(value="Console Output", style={'font_weight': 'bold'})
        self._clear_console_button = ipywidgets.Button(description="Clear", layout=ipywidgets.Layout(overflow='auto'))
        self._clear_console_button.on_click(self._clear_output_terminal)

        self._console_section_header = ipywidgets.HBox([self._console_description, self._clear_console_button],
                                                       layout=ipywidgets.Layout(justify_content='space-between',
                                                                                height='7%',
                                                                                padding_left='10px',
                                                                                padding_right='10px'))

        self._console_section_wrap = ipywidgets.VBox([self._console_section_header, self._console],
                                                     layout=ipywidgets.Layout(
                                                         overflow='auto', height='550px', padding='0px'))

        # Header Section
        self._header_wrap = ipywidgets.VBox([self._markdown_doc], layout=ipywidgets.Layout(
            overflow='auto', border='1px solid #ccc', padding='10px'))

        # Main Tab Layout
        self._tabs = ipywidgets.Tab(layout=ipywidgets.Layout(height='fit-content', ))
        self._tabs.children = [self._notebook_kernels_wrap, self._project_report_wrap, self._packages_section_wrap,
                               self._console_section_wrap]
        titles = ('Notebooks Overview', 'Projects Overview', 'Packages', 'Console Output')
        for i, title in enumerate(titles):
            self._tabs.set_title(i, title)

        version_label = ipywidgets.Label(value=f"Version: {self._version}")
        self._version = ipywidgets.HBox([version_label],
                                        layout=ipywidgets.Layout(justify_content='flex-end', height="fit-content"))

        super().__init__(children=[self._header_wrap, self._tabs, self._version])

        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = None

        self._update_notebook_kernels_wrap()
        if self._loop and self._loop.is_running():
            asyncio.create_task(self._update_packages_section_wrap())
            asyncio.create_task(self._update_projects_section_wrap())
        else:
            asyncio.run(self._update_packages_section_wrap())
            asyncio.run(self._update_projects_section_wrap())

    async def _update_projects_section_wrap(self):
        try:
            self._project_report_progress_bar.value += 10
            self.projects_df = pd.DataFrame(self._get_all_projects())
            self.projects_df.loc[self.projects_df["id"].isin(
                self._get_add_on_ids()), "project_type"] = "Data Lab Add-On"
            self.projects_df.loc[self.projects_df["id"].isin(
                self._get_packaged_add_on_ids()), "project_type"] = "Data Lab Packaged Add-On"
            self.projects_df['updated_at'] = self.projects_df.apply(
                lambda row: isoparse(row['updated_at'])
                .astimezone(self._user_timezone)
                .strftime(self._datetime_format), 
                axis=1
            )
            self.projects_df["name"] = self.projects_df.apply(lambda row: "<a href='{}' target='_blank'>{}</a>".format(
                urljoin(spy.session.public_url, f"data-lab/{row.id}"), row["name"]), axis=1)
            self._project_type_filter.options = ["All"] + list(self.projects_df["project_type"].unique())
            self._project_report_progress_bar.value = 100
            self._project_report_wrap.children = [self._project_report_controls, self._project_report_output]
            ipywidgets.interactive(self._filter_projects_dataframe,
                                   from_last_date=self._from_last_date_filter,
                                   scheduled_notebook=self._scheduled_notebook_filter,
                                   project_type=self._project_type_filter,
                                   sort_projects_by=self._sort_projects_by_filter
                                   )
        except Exception as e:
            self._project_report_wrap.children = [self._project_report_output]
            with self._project_report_output:
                self._project_report_output.clear_output()
                print(traceback.format_exc())

    def _update_notebook_kernels_wrap(self):
        try:
            self._parsed_notebooks = self._parse_notebooks(self._datalab_home)
            with self._notebook_kernels_output:
                self._notebook_kernels_output.clear_output()
                display(HTML(
                    self._full_width_table_css + self._parsed_notebooks.to_html(max_rows=None, max_cols=None,
                                                                                index=True,
                                                                                escape=False,
                                                                                table_id="full-width-table")))
        except Exception as e:
            with self._notebook_kernels_output:
                self._notebook_kernels_output.clear_output()
                print(traceback.format_exc())

    async def _update_packages_section_wrap(self):
        try:
            self._packages_section_progress_bar.value += 10
            self._packages = self._list_packages(self._config)
            self._packages_consolidated = self._consolidate(self._packages)
            selected_index = self._package_tabs.selected_index if self._package_tabs is not None else None
            self._package_tabs = self._create_package_tabs(self._packages_consolidated, self._config)
            if selected_index:
                self._package_tabs.selected_index = selected_index
            self._packages_section_progress_bar.value = 100
            self._packages_section_wrap.children = [self._package_tabs, self._package_install_box]
        except Exception as e:
            packages_output = ipywidgets.Output(layout=ipywidgets.Layout(overflow='auto', height='auto',
                                                                         padding='0px', display="grid"))

            self._packages_section_wrap.children = [packages_output]
            with packages_output:
                packages_output.clear_output()
                print(traceback.format_exc())

    def _generate_config(self):
        config = {}

        def _update_config(base_path, python, mode):
            site_packages_path = os.path.join(base_path, python, "site-packages", "")

            if os.path.isdir(site_packages_path):
                v = _parse_version(python)
                if v:
                    config.setdefault(v, {"site_package_path": {}})
                    config[v]["site_package_path"][mode] = site_packages_path

        def _update_config_for_base_path(base_path, mode):
            if os.path.isdir(base_path):
                for python_directory in os.listdir(base_path):
                    _update_config(base_path, python_directory, mode)

        def _parse_version(name):
            v = re.search(r'\d+\.\d+', name)
            return v.group(0) if v else None

        # Update config for local, global, and system Python installations
        _update_config_for_base_path(self._local_base_path, "local")
        _update_config_for_base_path(self._global_base_path, "global")

        if os.path.isdir(self._system_base_path):
            for path in os.listdir(self._system_base_path):
                system_lib_path = os.path.join(self._system_base_path, path, "lib")
                version = _parse_version(path)
                if version:
                    config.setdefault(version, {"site_package_path": {}})
                    config[version]["pip_path"] = os.path.join(self._system_base_path, path, "bin", "pip")
                    config[version]["python_path"] = os.path.join(self._system_base_path, path, "bin", "python")
                if os.path.isdir(system_lib_path):
                    for python_dir in os.listdir(system_lib_path):
                        if python_dir.startswith("python"):
                            _update_config(system_lib_path, python_dir, "system")

        return config

    def _list_packages_in_site_packages(self, site_packages_path):
        from importlib.metadata import distributions

        packages = {}
        try:
            distributions = distributions(path=[site_packages_path])
            for item in distributions:
                if item.name is None:
                    continue
                packages[item.name] = {"project_name": item.name, "version": item.version}
        except Exception as e:
            print(f"Error listing packages in {site_packages_path}: {e}")
        return packages

    def _list_packages(self, config):
        result = {}
        for version, c in config.items():
            v_result = {}
            for mode, path in c.get("site_package_path", {}).items():
                v_result[mode] = self._list_packages_in_site_packages(path)
                self._packages_section_progress_bar.value += 10
            result[version] = v_result
        return result

    def _consolidate(self, packages):
        from collections import defaultdict
        result = defaultdict(lambda: defaultdict(dict))
        for version, item in packages.items():
            for k in self._categories:
                for package, detail in item.get(k, {}).items():
                    result[k][package][version] = detail
        return result

    def _create_table_grid(self, packages, config, mode="local"):

        def _version_key(v):
            major, minor = map(int, v.split('.'))
            return major, minor

        def get_ui_item(package, version, item, mode):
            if item:
                return item.get('version')
            pip_path = self._config.get(version, {}).get("pip_path", None)
            if not pip_path:
                return "-"
            if mode == "local":
                return self._create_install_button("Install Locally", package, pip_path, mode)
            if mode == "global":
                if self._has_global_write_access:
                    return self._create_install_button("Install Globally", package, pip_path, mode)
                else:
                    return ipywidgets.Button(description="Ask Admin to Install", disabled=True)
            return "-"

        def generate_rows():
            all_python_versions = sorted(config.keys(), key=_version_key)
            for package, v in sorted(packages.items()):
                row = [package]
                for version in all_python_versions:
                    item = v.get(version)
                    row.append(get_ui_item(package, version, item, mode))
                yield row

        headers = ["Package Name"] + [f"Python {v}" for v in sorted(config.keys(), key=_version_key)]
        table_data = list(generate_rows())

        # Create header and row widgets
        header_widgets = [ipywidgets.Label(value=header, style={'font_weight': 'bold'}) for header in headers]
        row_widgets = [ipywidgets.Label(value=str(cell)) if isinstance(cell, str) else cell for row in table_data for
                       cell in row]

        return ipywidgets.GridBox(header_widgets + row_widgets, layout=ipywidgets.Layout(
            grid_template_columns=f'40% repeat({len(headers) - 1}, auto)',
            grid_gap='2px',
            padding='5px'
        ))

    def _create_install_button(self, description, package, pip_path, mode):
        button = ipywidgets.Button(description=description)
        button.on_click(lambda btn: self._install_package(package, pip_path, mode, btn))
        return button

    def _create_package_tabs(self, packages, config):
        tab_contents = {}
        for category in self._categories:
            content = self._create_table_grid(packages[category], config,
                                              mode=category)
            tab_contents[category] = content

        # Create a Tab widget and add content
        tab = ipywidgets.Tab(layout=ipywidgets.Layout(overflow='auto', height='93%', padding='0px'))
        tab.children = [tab_contents[cat] for cat in self._categories]

        # Set tab titles
        for i, category in enumerate(self._categories):
            tab.set_title(i, f"{category} packages".capitalize())

        return tab

    def _general_install_packages(self, b):
        package_name = self._package_input.value
        mode = self._package_scope_dropdown.value
        version = self._package_version_dropdown.value
        pip_path = self._config.get(version, {}).get("pip_path")

        if package_name and mode and pip_path:
            self._package_input.value = ''
            self._install_package(package_name, pip_path, mode)

    def _install_package(self, package, pip_path, mode, button=None):
        import subprocess
        from IPython.display import clear_output
        self._tabs.selected_index = 3
        if button:
            button.disabled = True
            button.description = "Installing"
        with self._console:
            clear_output(wait=True)
            print(f"Installing latest version of {package} ...")
            try:
                env = os.environ.copy()
                install_commands = [pip_path, 'install']
                if mode == "global":
                    env['PYTHONUSERBASE'] = self._global_base
                    install_commands.append("--ignore-installed")
                subprocess.run(install_commands + [package], env=env, check=True)
                if button:
                    button.description = "Installed"
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}:")
                if e.stderr:
                    print(e.stderr.decode('utf-8'))
                if button:
                    button.description = "Install Locally"
                    button.disabled = False
        if self._loop and self._loop.is_running():
            asyncio.create_task(self._update_packages_section_wrap())
        else:
            asyncio.run(self._update_packages_section_wrap())

    def _clear_output_terminal(self, button):
        from IPython.display import clear_output
        with self._console:
            clear_output()

    def _parse_notebooks(self, directory="."):
        data = []
        ignore_folders = {'SPy Documentation'}

        def add_to_data(path, last_modified, kernel):
            parts = path.split(os.sep)
            dir_path = os.sep.join(parts[:-1])
            file_name = parts[-1]
            data.append((dir_path, file_name, last_modified, kernel))

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_folders]

            for file in files:
                if file.endswith('.ipynb'):
                    abs_path = os.path.join(root, file)
                    path = os.path.relpath(abs_path, start=directory)
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        nb = nbformat.read(f, as_version=4)
                        kernel = nb.get('metadata', {}).get('kernelspec', {}).get('display_name', '-')
                    last_modified_time = datetime.fromtimestamp(os.path.getmtime(abs_path)).astimezone(self._user_timezone)
                    last_modified = last_modified_time.strftime(self._datetime_format)

                    add_to_data(path, last_modified, kernel)

        # Create a MultiIndex DataFrame
        index = pd.MultiIndex.from_tuples(data, names=['Directory', 'Notebook Name', 'Last Modified',
                                                       'Selected Kernel'])
        return pd.DataFrame(index=index).sort_values(by=['Directory', 'Notebook Name'])

    def _get_all_projects(self, ):
        prev = 0
        limit = 1000
        name_max_length = 38
        project_type_map = {"DATA_LAB": "Data Lab", "DATA_LAB_FUNCTIONS": "Data Lab Functions"}
        projects = []
        projects_api = ProjectsApi(spy.session.client)
        self._project_report_progress_bar.value += 10
        while True:
            resp = projects_api.get_projects(offset=prev, limit=limit)
            prev += limit
            for project in resp.projects:
                x = dict()
                x["name"] = project.name if len(project.name) <= name_max_length \
                    else project.name[:name_max_length - 3] + '...'
                x["type"] = project.type
                x["id"] = project.id
                x["owner_name"] = project.owner.name if project.owner else None
                x["creator_name"] = project.creator.name if project.creator else None
                x["project_type"] = project_type_map.get(project.project_type, "Data Lab")
                x["updated_at"] = project.updated_at
                scheduled_notebook_status = 'None'
                if project.scheduled_notebooks:
                    if any(not schedule.stopped for sn in project.scheduled_notebooks for schedule in sn.schedules):
                        scheduled_notebook_status = 'Active'
                    elif all(schedule.stopped for sn in project.scheduled_notebooks for schedule in sn.schedules):
                        scheduled_notebook_status = 'Stopped'
                x['scheduled_notebooks'] = scheduled_notebook_status
                projects.append(x)
            self._project_report_progress_bar.value += 10
            if resp.next is None:
                break
        return projects

    def _get_add_on_ids(self):
        def extract_id(url):
            pattern = r'/([0-9A-F-]{36})/'
            match = re.search(pattern, url)
            return match.group(1) if match else None

        try:
            system_api = SystemApi(spy.session.client)
            return [
                id for tool in system_api.get_add_on_tools().add_on_tools
                if (id := extract_id(tool.target_url)) is not None
            ]
        except Exception as e:
            return []

    def _get_packaged_add_on_ids(self):

        def is_adopted_addon(add_on_identifier):
            import uuid
            uuid_string = add_on_identifier.split(".")[-1]
            try:
                uuid_obj = uuid.UUID(uuid_string, version=4)
                return str(uuid_obj) == uuid_string
            except ValueError:
                return False

        add_on_api = AddOnsApi(spy.session.client)
        prev = 0
        limit = 1000
        packaged_addon_ids = []
        try:
            while True:
                resp = add_on_api.get_add_ons(offset=prev, limit=limit)
                prev += limit
                for ao in resp.add_ons:
                    # The Adopted add-on have the version_string as 0.0.1
                    if ao.version_string == "0.0.1" and is_adopted_addon(ao.add_on_identifier):
                        continue
                    aoc = json.loads(ao.add_on_components)
                    for v in aoc.get("elements", {}).values():
                        if v.get("infrastructure_type") == "AddOnTool":
                            project_id = v.get("properties", {}).get("projectId")
                            if project_id:
                                packaged_addon_ids.append(project_id)
                                break
                if resp.next is None:
                    break
        except Exception as e:
            pass
        return packaged_addon_ids

    def _filter_projects_dataframe(self, from_last_date, scheduled_notebook, project_type, sort_projects_by):

        today = datetime.utcnow()

        # Determine start date based on the selected filter
        date_options = {
            'Last 1 Month': 30,
            'Last 3 Months': 90,
            'Last 6 Months': 180,
            'Last 1 Year': 365
        }

        if from_last_date in date_options:
            start_date = today - timedelta(days=date_options[from_last_date])
        else:
            start_date = pd.Timestamp.min

        start_date = start_date.astimezone(self._user_timezone).strftime(self._datetime_format)
        filtered_df = self.projects_df[self.projects_df['updated_at'] >= start_date]
        if project_type != 'All':
            filtered_df = filtered_df[filtered_df['project_type'] == project_type]
        if scheduled_notebook != 'All':
            filtered_df = filtered_df[filtered_df['scheduled_notebooks'] == scheduled_notebook]
        if sort_projects_by == "Last Updated":
            filtered_df = filtered_df.sort_values(by='updated_at', ascending=False).reset_index(drop=True)
        elif sort_projects_by == "Project Name":
            filtered_df = filtered_df.sort_values(by='name', ascending=True).reset_index(drop=True)
        filtered_df.index += 1

        # Rename columns and format DataFrame for display
        filtered_df = filtered_df[
            ['name', 'id', 'owner_name', 'creator_name', 'project_type', 'updated_at', 'scheduled_notebooks']]

        filtered_df = filtered_df.rename(columns={
            'name': 'Project Name',
            'id': 'ID',
            'owner_name': 'Owner Name',
            'creator_name': 'Creator Name',
            'project_type': 'Project Type',
            'updated_at': 'Last Updated',
            'scheduled_notebooks': "Scheduled Notebooks"
        })

        # Display the DataFrame
        with self._project_report_output:
            self._project_report_output.clear_output()
            display(HTML(
                self._full_width_table_css + filtered_df.to_html(max_rows=None, max_cols=None, index=True, escape=False,
                                                                 table_id="full-width-table")))
