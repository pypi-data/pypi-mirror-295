from IPython.display import display
from ipywidgets import widgets

adapter_dropdown = widgets.Dropdown(
    options=[('--Seleccione --', ""),
             ("Hdfs-Staging", "hdfs-staging"),
             ("Hdfs-OutStaging", "hdfs-outstaging"),
             ("Hdfs-Master", "hdfs-master"),
             ("Launchpad", "gcs"),
             ("OraclePE", "oraclepe"),
             ("Oracle Custom", "oracle-custom"),
             ("CONNECT Host", "connectdirect-host"),
             ("CONNECT Xcom Oficinas", "connectdirect-oficina"),
             ("CONNECT Spectrum", "connectdirect-spectrum"),
             ("CONNECT PIC", "connectdirect-pic"),
             ("ElasticSearch", "elasticSearch"),
             ("SalesforcePE", "salesforcepe"),
             ("SftpPE Eglobal", "sftp-eglobal"),
             ("SftpPE Openpay", "sftp-openpay"),
             ("SftpPE Int. o ext. Custom", "sftp-int-ext"),
             ("BTS", "bts"),
             ],
    value='',
    description='Adapter:',
    disabled=False
)
text_uuaa_name = widgets.Text(
    value='',
    placeholder='UUAA Name',
    description='UUAA Name:',
    disabled=False
)

text_country = widgets.Dropdown(
    options=[('--Seleccione --', ""),
             ("PERU", "pe"),
             ("MEXICO", "mx"),
             ("ESPAÑA", "es"),
             ("ARGENTINA", "ar"),
             ("COLOMBIA", "co"),
             ],
    value='pe',
    description='Country:',
    disabled=False
)
text_schema = widgets.Text(
    value='',
    placeholder='Schema',
    description='Schema:',
    disabled=False
)

text_nro_oficina = widgets.Text(
    value='',
    placeholder='Nro Oficina',
    description='Nro Oficina:',
    disabled=False
)
text_process_name = widgets.Text(
    value='',
    placeholder='Process Name',
    description='Process Name:',
    disabled=False
)

button_generated = widgets.Button(
    description='Generate Adapter',
    disabled=False,
    button_style='primary'
)
out = widgets.Output()
text_required = widgets.HTML(value="")
btn_required = widgets.HTML(value="")
result_adapter = widgets.HTML(value="")

box_hdfs_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_country
    ]
)
box_gcs_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_country
    ]
)
box_connectdirect_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_country
    ]
)
box_connectdirect_oficina = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_nro_oficina,
        text_country
    ]
)
box_oracle_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_schema,
        text_country
    ]
)
box_elasticsearch_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_schema,
        text_country
    ]
)
box_salesforce_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_process_name,
        text_country
    ]
)
box_sftp_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_country
    ]
)

box_sftp_custom = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_process_name,
        text_country

    ]
)
box_bts_generic = widgets.VBox(
    [
        text_required,
        text_uuaa_name,
        text_country
    ]
)

box_button_generated = widgets.VBox(
    [
        button_generated,
        result_adapter,
        btn_required
    ]
)


def load_select_datax():
    display(adapter_dropdown)
    display(out)

    def on_upload_change(change):
        out.clear_output()
        result_adapter.value = ""
        if change['new'] in ("hdfs-staging", "hdfs-outstaging", "hdfs-master"):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_hdfs_generic)
                display(box_button_generated)
        elif change['new'] in ("gcs",):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_gcs_generic)
                display(box_button_generated)
        elif change['new'] in ("connectdirect-oficina",):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_connectdirect_oficina)
                display(box_button_generated)
        elif change['new'] in ("connectdirect-host", "connectdirect-spectrum", "connectdirect-pic"):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_connectdirect_generic)
                display(box_button_generated)

        elif change['new'] in ("oraclepe", "oracle-custom"):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_oracle_generic)
                display(box_button_generated)
        elif change['new'] in ("elasticSearch",):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_elasticsearch_generic)
                display(box_button_generated)
        elif change['new'] in ("salesforcepe",):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_salesforce_generic)
                display(box_button_generated)
        elif change['new'] in ("sftp-eglobal", "sftp-openpay"):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_sftp_generic)
                display(box_button_generated)

        elif change['new'] in ("sftp-int-ext",):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_sftp_custom)
                display(box_button_generated)

        elif change['new'] in ("bts",):
            with out:
                text_required.value = f"<b>--Parameters {change['new']}--</b>"
                display(box_bts_generic)
                display(box_button_generated)

    adapter_dropdown.observe(on_upload_change, names='value')


def evaluate_adapter_generated(_):
    text_req = str(text_required.value).replace("<b>", "").replace("</b>", "").replace("--", "").split(" ")
    text_req = str(text_req[1]).strip()
    if text_req in ("hdfs-staging", "hdfs-outstaging", "hdfs-master",
                    "gcs", "connectdirect-host", "connectdirect-spectrum",
                    "connectdirect-pic", "sftp-eglobal", "sftp-openpay",
                    "bts"):

        if text_uuaa_name.value == "":
            btn_required.value = f"<b>Required UUAA</b>"
        elif len(text_uuaa_name.value) < 4:
            btn_required.value = f"<b>Required UUAA 4 Character</b>"
        elif text_country.value == "":
            btn_required.value = f"<b>Required Country</b>"
        else:
            if text_req == "hdfs-staging":
                rs = generated_hdfs_staging(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "hdfs-outstaging":
                rs = generated_hdfs_outstaging(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "hdfs-master":
                rs = generated_hdfs_master(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "gcs":
                rs = generated_gcs(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "connectdirect-host":
                rs = generated_connectdirect_host(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "connectdirect-spectrum":
                rs = generated_connectdirect_spectrum(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "connectdirect-pic":
                rs = generated_connectdirect_pic(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "sftp-eglobal":
                rs = generated_sftp_eglobal(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "sftp-openpay":
                rs = generated_sftp_openpay(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            if text_req == "bts":
                rs = generated_bts(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs
            text_uuaa_name.value = ""
            text_country.value = ""

    elif text_req in ("connectdirect-oficina",):
        if text_uuaa_name.value == "":
            btn_required.value = f"<b>Required UUAA</b>"
        elif len(text_uuaa_name.value) < 4:
            btn_required.value = f"<b>Required UUAA 4 Character</b>"
        elif text_country.value == "":
            btn_required.value = f"<b>Required Country</b>"
        elif text_nro_oficina.value == "":
            btn_required.value = f"<b>Required Nro Oficina</b>"
        else:
            if text_req == "connectdirect-oficina":
                rs = generated_connectdirect_oficine(uuaa_master=text_uuaa_name.value, country=text_country.value, nro_oficina=text_nro_oficina.value)
                result_adapter.value = rs
            text_uuaa_name.value = ""
            text_country.value = ""
            text_nro_oficina.value = ""

    elif text_req in ("oraclepe", "oracle-custom", "elasticSearch"):
        if text_uuaa_name.value == "":
            btn_required.value = f"<b>Required UUAA</b>"
        elif len(text_uuaa_name.value) < 4:
            btn_required.value = f"<b>Required UUAA 4 Character</b>"
        elif text_country.value == "":
            btn_required.value = f"<b>Required Country</b>"
        elif text_schema.value == "":
            btn_required.value = f"<b>Required Schema Database</b>"
        else:
            if text_req == "oraclepe":
                rs = generated_oracle_pe(uuaa_master=text_uuaa_name.value, country=text_country.value, schema_oracle=text_schema.value)
                result_adapter.value = rs
            if text_req == "oracle-custom":
                rs = generated_oracle_custom(uuaa_master=text_uuaa_name.value, country=text_country.value, schema_oracle=text_schema.value)
                result_adapter.value = rs
            if text_req == "elasticSearch":
                rs = generated_elasticsearch_custom(uuaa_master=text_uuaa_name.value, country=text_country.value, schema_elasticsearch=text_schema.value)
                result_adapter.value = rs

            text_uuaa_name.value = ""
            text_country.value = ""
            text_schema.value = ""

    elif text_req in ("salesforcepe", "sftp-int-ext"):
        if text_uuaa_name.value == "":
            btn_required.value = f"<b>Required UUAA</b>"
        elif len(text_uuaa_name.value) < 4:
            btn_required.value = f"<b>Required UUAA 4 Character</b>"
        elif text_country.value == "":
            btn_required.value = f"<b>Required Country</b>"
        elif text_process_name.value == "":
            btn_required.value = f"<b>Required Process Name</b>"
        else:
            if text_req == "salesforcepe":
                rs = generated_salesforce_pe(uuaa_master=text_uuaa_name.value, country=text_country.value, process_name=text_process_name.value)
                result_adapter.value = rs
            if text_req == "sftp-int-ext":
                rs = generated_sftp_custom(uuaa_master=text_uuaa_name.value, country=text_country.value, process_name=text_process_name.value)
                result_adapter.value = rs

            text_uuaa_name.value = ""
            text_country.value = ""
            text_process_name.value = ""

    elif text_req in ("bts",):
        if text_uuaa_name.value == "":
            btn_required.value = f"<b>Required UUAA</b>"
        elif len(text_uuaa_name.value) < 4:
            btn_required.value = f"<b>Required UUAA 4 Character</b>"
        elif text_country.value == "":
            btn_required.value = f"<b>Required Country</b>"
        else:
            if text_req == "bts":
                rs = generated_bts(uuaa_master=text_uuaa_name.value, country=text_country.value)
                result_adapter.value = rs

            text_uuaa_name.value = ""
            text_country.value = ""
            text_process_name.value = ""


button_generated.on_click(evaluate_adapter_generated)


def generated_hdfs_staging(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('hdfs.html')
    title_html = "HDFS STAGING - hdfs.v2"

    au_adapter_id = f"adapter-hdfsstaging-{uuaa_master.lower()}-v0"
    au_adapter_connection_id = f"con-pe-adapter-hdfsstaging-{uuaa_master.lower()}-au-v0"
    au_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} Staging Zone in au"
    au_adapter_tenant = f"{country.lower()}"
    au_adapter_basepath = f"/in/staging/datax/{uuaa_master.lower()}"

    dev_adapter_id = f"adapter-hdfsstaging-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-hdfsstaging-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} Staging Zone in dev"
    dev_adapter_tenant = f"{country.lower()}"
    dev_adapter_basepath = f"/in/staging/datax/{uuaa_master.lower()}"

    pro_adapter_id = f"adapter-hdfsstaging-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-hdfsstaging-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} Staging Zone in pro"
    pro_adapter_tenant = f"{country.lower()}"
    pro_adapter_basepath = f"/in/staging/datax/{uuaa_master.lower()}"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_tenant=au_adapter_tenant,
        au_adapter_basepath=au_adapter_basepath,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_tenant=dev_adapter_tenant,
        dev_adapter_basepath=dev_adapter_basepath,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_tenant=pro_adapter_tenant,
        pro_adapter_basepath=pro_adapter_basepath,
    )

    return output


def generated_hdfs_outstaging(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('hdfs.html')
    title_html = "HDFS OUTSTAGING - hdfs.v2"

    au_adapter_id = f"adapter-hdfsoutstaging-{uuaa_master.lower()}-v0"
    au_adapter_connection_id = f"con-pe-adapter-hdfsoutstaging-{uuaa_master.lower()}-au-v0"
    au_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} OutStaging Zone in au"
    au_adapter_tenant = f"{country.lower()}"
    au_adapter_basepath = f"out/staging/ratransmit/{uuaa_master.lower()}"

    dev_adapter_id = f"adapter-hdfsoutstaging-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-hdfsoutstaging-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} OutStaging Zone in dev"
    dev_adapter_tenant = f"{country.lower()}"
    dev_adapter_basepath = f"/out/staging/ratransmit/{uuaa_master.lower()}"

    pro_adapter_id = f"adapter-hdfsoutstaging-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-hdfsoutstaging-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} OutStaging Zone in pro"
    pro_adapter_tenant = f"{country.lower()}"
    pro_adapter_basepath = f"/out/staging/ratransmit/{uuaa_master.lower()}"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_tenant=au_adapter_tenant,
        au_adapter_basepath=au_adapter_basepath,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_tenant=dev_adapter_tenant,
        dev_adapter_basepath=dev_adapter_basepath,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_tenant=pro_adapter_tenant,
        pro_adapter_basepath=pro_adapter_basepath,
    )
    return output


def generated_hdfs_master(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('hdfs.html')
    title_html = "HDFS MASTER - hdfs.master"

    au_adapter_id = f"adapter-hdfsmaster-{uuaa_master.lower()}-v0"
    au_adapter_connection_id = f"con-pe-adapter-hdfsmaster-{uuaa_master.lower()}-au-v0"
    au_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} OutStaging Zone in au"
    au_adapter_tenant = f"{country.lower()}"
    au_adapter_basepath = f"/data/master/{uuaa_master.lower()}/data"

    dev_adapter_id = f"adapter-hdfsmaster-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-hdfsmaster-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} OutStaging Zone in dev"
    dev_adapter_tenant = f"{country.lower()}"
    dev_adapter_basepath = f"/data/master/{uuaa_master.lower()}/data"

    pro_adapter_id = f"adapter-hdfsmaster-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-hdfsmaster-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter HDFS in UUAA {uuaa_master.upper()} OutStaging Zone in pro"
    pro_adapter_tenant = f"{country.lower()}"
    pro_adapter_basepath = f"/data/master/{uuaa_master.lower()}/data"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_tenant=au_adapter_tenant,
        au_adapter_basepath=au_adapter_basepath,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_tenant=dev_adapter_tenant,
        dev_adapter_basepath=dev_adapter_basepath,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_tenant=pro_adapter_tenant,
        pro_adapter_basepath=pro_adapter_basepath,
    )
    return output


def generated_gcs(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('gcs.html')
    title_html = "GCS - gcs.bbva"

    au_adapter_id = f"adapter-gcslaunchpad-{uuaa_master.lower()}-v0"
    au_adapter_connection_id = f"con-pe-adapter-gcslaunchpad-{uuaa_master.lower()}-au-v0"
    au_adapter_desc = f"Adapter GCS in UUAA {uuaa_master.upper()} in au"
    au_adapter_bucket = f"au-bbva-launchpad-sp-out_{country.lower()}r"
    au_adapter_project_id = f"au-bbva-launchpad-sp"

    dev_adapter_id = f"adapter-gcslaunchpad-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-gcslaunchpad-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter GCS in UUAA {uuaa_master.upper()} in dev"
    dev_adapter_bucket = f"dev-bbva-launchpad-sp-out_{country.lower()}r"
    dev_adapter_project_id = f"dev-bbva-launchpad-sp"

    pro_adapter_id = f"adapter-gcslaunchpad-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-gcslaunchpad-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter GCS in UUAA {uuaa_master.upper()} in pro"
    pro_adapter_bucket = f"bbva-launchpad-sp-out_{country.lower()}r"
    pro_adapter_project_id = f"bbva-launchpad-sp"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_bucket=au_adapter_bucket,
        au_adapter_project_id=au_adapter_project_id,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_bucket=dev_adapter_bucket,
        dev_adapter_project_id=dev_adapter_project_id,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_bucket=pro_adapter_bucket,
        pro_adapter_project_id=pro_adapter_project_id,
    )
    return output


def generated_connectdirect_oficine(uuaa_master=None, country=None, nro_oficina=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('connect_direct.html')
    title_html = "XCOM OFICINAS - connectdirect.pe.unix"

    au_adapter_id = f"adapter-connectdirectxcom-{uuaa_master.lower()}of{nro_oficina.lower()}-v0"
    au_adapter_connection_id = f"con-pe-adapter-connectdirectxcom-{uuaa_master.lower()}of{nro_oficina.lower()}-au-v0"
    au_adapter_desc = f"Adapter CONNECTDIRECT in UUAA PMOL OF{nro_oficina.upper()} in au"
    au_adapter_basepath = f"/BBVA/S7729600VM/xcomntip/OF_{nro_oficina.upper()}"
    au_adapter_snode = f"118.180.60.121"
    au_adapter_operating_system = f"Unix"
    au_adapter_sport = f"1364"

    dev_adapter_id = f"adapter-connectdirectxcom-{uuaa_master.lower()}of{nro_oficina.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-connectdirectxcom-{uuaa_master.lower()}of{nro_oficina.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter CONNECTDIRECT in UUAA PMOL OF{nro_oficina.upper()} in dev"
    dev_adapter_basepath = f"/BBVA/S7729600VM/xcomntip/OF_{nro_oficina.upper()}"
    dev_adapter_snode = f"118.180.60.121"
    dev_adapter_operating_system = f"Unix"
    dev_adapter_sport = f"1364"

    pro_adapter_id = f"adapter-connectdirectxcom-{uuaa_master.lower()}of{nro_oficina.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-connectdirectxcom-{uuaa_master.lower()}of{nro_oficina.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter CONNECTDIRECT in UUAA PMOL OF{nro_oficina.upper()} in pro"
    pro_adapter_basepath = f"/BBVA/S7729600VM/xcomntip/OF_{nro_oficina.upper()}"
    pro_adapter_snode = f"118.180.60.121"
    pro_adapter_operating_system = f"Unix"
    pro_adapter_sport = f"1364"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_snode=au_adapter_snode,
        au_adapter_operating_system=au_adapter_operating_system,
        au_adapter_sport=au_adapter_sport,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_snode=dev_adapter_snode,
        dev_adapter_operating_system=dev_adapter_operating_system,
        dev_adapter_sport=dev_adapter_sport,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_snode=pro_adapter_snode,
        pro_adapter_operating_system=pro_adapter_operating_system,
        pro_adapter_sport=pro_adapter_sport
    )
    return output


def generated_connectdirect_host(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('connect_direct.html')
    title_html = "HOST - connectdirect.pe.host"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_basepath = f""
    au_adapter_snode = f""
    au_adapter_operating_system = f""
    au_adapter_sport = f""

    dev_adapter_id = f"adapter-connectdirecthost-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-connectdirecthost-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirecthost files in dev"
    dev_adapter_basepath = f"PEBD"
    dev_adapter_snode = f"150.250.40.145"
    dev_adapter_operating_system = f"zos"
    dev_adapter_sport = f"1364"

    pro_adapter_id = f"adapter-connectdirecthost-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-connectdirecthost-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirecthost files in pro"
    pro_adapter_basepath = f"PEBP"
    pro_adapter_snode = f"150.250.40.21"
    pro_adapter_operating_system = f"zos"
    pro_adapter_sport = f"1364"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_snode=au_adapter_snode,
        au_adapter_operating_system=au_adapter_operating_system,
        au_adapter_sport=au_adapter_sport,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_snode=dev_adapter_snode,
        dev_adapter_operating_system=dev_adapter_operating_system,
        dev_adapter_sport=dev_adapter_sport,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_snode=pro_adapter_snode,
        pro_adapter_operating_system=pro_adapter_operating_system,
        pro_adapter_sport=pro_adapter_sport
    )
    return output


def generated_connectdirect_spectrum(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('connect_direct.html')
    title_html = "SPECTRUM - connectdirect.pe.unix"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_basepath = f""
    au_adapter_snode = f""
    au_adapter_operating_system = f""
    au_adapter_sport = f""

    dev_adapter_id = f"adapter-connectdirectspectrum-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-connectdirectspectrum-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirectspectrum files in dev"
    dev_adapter_basepath = f"/BBVA/PWAPBDVTRUM01"
    dev_adapter_snode = f"118.180.60.121"
    dev_adapter_operating_system = f"Unix"
    dev_adapter_sport = f"1364"

    pro_adapter_id = f"adapter-connectdirectspectrum-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-connectdirectspectrum-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirectspectrum files in pro"
    pro_adapter_basepath = f"/BBVA/PWAPBDVTRUM01"
    pro_adapter_snode = f"118.180.60.121"
    pro_adapter_operating_system = f"Unix"
    pro_adapter_sport = f"1364"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_snode=au_adapter_snode,
        au_adapter_operating_system=au_adapter_operating_system,
        au_adapter_sport=au_adapter_sport,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_snode=dev_adapter_snode,
        dev_adapter_operating_system=dev_adapter_operating_system,
        dev_adapter_sport=dev_adapter_sport,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_snode=pro_adapter_snode,
        pro_adapter_operating_system=pro_adapter_operating_system,
        pro_adapter_sport=pro_adapter_sport
    )
    return output


def generated_connectdirect_pic(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('connect_direct.html')
    title_html = "PIC - connectdirect.pe.unix"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_basepath = f""
    au_adapter_snode = f""
    au_adapter_operating_system = f""
    au_adapter_sport = f""

    dev_adapter_id = f"adapter-connectdirectpic-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-connectdirectpic-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirectpic files in dev"
    dev_adapter_basepath = f"/filespic/out"
    dev_adapter_snode = f"150.250.242.60"
    dev_adapter_operating_system = f"Unix"
    dev_adapter_sport = f"1364"

    pro_adapter_id = f"adapter-connectdirectpic-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-connectdirectpic-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirectpic files in pro"
    pro_adapter_basepath = f"/filespic/out"
    pro_adapter_snode = f"150.250.242.60"
    pro_adapter_operating_system = f"Unix"
    pro_adapter_sport = f"1364"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_snode=au_adapter_snode,
        au_adapter_operating_system=au_adapter_operating_system,
        au_adapter_sport=au_adapter_sport,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_snode=dev_adapter_snode,
        dev_adapter_operating_system=dev_adapter_operating_system,
        dev_adapter_sport=dev_adapter_sport,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_snode=pro_adapter_snode,
        pro_adapter_operating_system=pro_adapter_operating_system,
        pro_adapter_sport=pro_adapter_sport
    )
    return output


def generated_connectdirect_sterlin(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('connect_direct.html')
    title_html = "STERLIN OPENPAY - connectdirect.pe.unix"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_basepath = f""
    au_adapter_snode = f""
    au_adapter_operating_system = f""
    au_adapter_sport = f""

    dev_adapter_id = f"adapter-connectdirectmailboxopenpay-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-connectdirectmailboxopenpay-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirectmailboxopenpay files in dev"
    dev_adapter_basepath = f"/mailbox/padq/openpay"
    dev_adapter_snode = f"118.180.34.70"
    dev_adapter_operating_system = f"Unix"
    dev_adapter_sport = f"1364"

    pro_adapter_id = f"adapter-connectdirectmailboxopenpay-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-connectdirectmailboxopenpay-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter CONNECTDIRECT in UUAA {uuaa_master.upper()} connectdirectmailboxopenpay files in pro"
    pro_adapter_basepath = f"/mailbox/padq/openpay"
    pro_adapter_snode = f"118.180.54.113"
    pro_adapter_operating_system = f"Unix"
    pro_adapter_sport = f"1364"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_snode=au_adapter_snode,
        au_adapter_operating_system=au_adapter_operating_system,
        au_adapter_sport=au_adapter_sport,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_snode=dev_adapter_snode,
        dev_adapter_operating_system=dev_adapter_operating_system,
        dev_adapter_sport=dev_adapter_sport,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_snode=pro_adapter_snode,
        pro_adapter_operating_system=pro_adapter_operating_system,
        pro_adapter_sport=pro_adapter_sport
    )
    return output


def generated_oracle_pe(uuaa_master=None, country=None, schema_oracle=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('oraclepe.html')
    title_html = "Oracle Peru - oracle.pe"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_host = ""
    au_adapter_service = f""
    au_adapter_port = f""

    dev_adapter_id = f"adapter-oraclepe{schema_oracle.lower()}-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-oraclepe{schema_oracle.lower()}-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter ORACLE in UUAA {uuaa_master.upper()} oraclepe{schema_oracle.lower()} files in dev"
    dev_adapter_host = "118.180.35.45"
    dev_adapter_service = f"tst12c"
    dev_adapter_port = f"1521"

    pro_adapter_id = f"adapter-oraclepe{schema_oracle.lower()}-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-oraclepe{schema_oracle.lower()}-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter ORACLE in UUAA {uuaa_master.upper()} oraclepe{schema_oracle.lower()} files in pro"
    pro_adapter_host = "118.180.61.137"
    pro_adapter_service = f"ora12c"
    pro_adapter_port = f"1521"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_host=au_adapter_host,
        au_adapter_service=au_adapter_service,
        au_adapter_port=au_adapter_port,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_host=dev_adapter_host,
        dev_adapter_service=dev_adapter_service,
        dev_adapter_port=dev_adapter_port,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_host=pro_adapter_host,
        pro_adapter_service=pro_adapter_service,
        pro_adapter_port=pro_adapter_port
    )
    return output


def generated_oracle_custom(uuaa_master=None, country=None, schema_oracle=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('oraclepe.html')
    title_html = "Oracle EXTERNAL - oracle.physics"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_host = ""
    au_adapter_service = f""
    au_adapter_port = f""

    dev_adapter_id = f"adapter-oracle{schema_oracle.lower()}-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-oracle{schema_oracle.lower()}-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter ORACLE in UUAA {uuaa_master.upper()} oracle{schema_oracle.lower()} files in dev"
    dev_adapter_host = ""
    dev_adapter_service = f""
    dev_adapter_port = f"1521"

    pro_adapter_id = f"adapter-oracle{schema_oracle.lower()}-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-oracle{schema_oracle.lower()}-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter ORACLE in UUAA {uuaa_master.upper()} oracle{schema_oracle.lower()} files in pro"
    pro_adapter_host = ""
    pro_adapter_service = f""
    pro_adapter_port = f"1521"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_host=au_adapter_host,
        au_adapter_service=au_adapter_service,
        au_adapter_port=au_adapter_port,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_host=dev_adapter_host,
        dev_adapter_service=dev_adapter_service,
        dev_adapter_port=dev_adapter_port,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_host=pro_adapter_host,
        pro_adapter_service=pro_adapter_service,
        pro_adapter_port=pro_adapter_port
    )
    return output


def generated_elasticsearch_custom(uuaa_master=None, country=None, schema_elasticsearch=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('elasticsearch.html')
    title_html = "ElastiSearch - Elastic.iaas"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_urlstring = ""
    au_adapter_batchsize = f""
    au_adapter_physicaldbname = f""

    dev_adapter_id = f"adapter-elastisearch{schema_elasticsearch.lower()}-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-elastisearch{schema_elasticsearch.lower()}-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter ELASTICSEARCH in UUAA {uuaa_master.upper()} elastisearch{schema_elasticsearch.lower()} files in dev"
    dev_adapter_urlstring = f"https://elas.work.mx.nextgen.igrupobbva:9201"
    dev_adapter_batchsize = f"2058"
    dev_adapter_physicaldbname = f"{schema_elasticsearch.upper()}"

    pro_adapter_id = f"adapter-elastisearch{schema_oracle.lower()}-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-elastisearch{schema_elasticsearch.lower()}-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter ELASTICSEARCH in UUAA {uuaa_master.upper()} elastisearch{schema_elasticsearch.lower()} files in pro"
    pro_adapter_urlstring = f"https://elas.live.mx.nextgen.igrupobbva:9201"
    pro_adapter_batchsize = f"2058"
    pro_adapter_physicaldbname = f"{schema_elasticsearch.upper()}"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_urlstring=au_adapter_urlstring,
        au_adapter_batchsize=au_adapter_batchsize,
        au_adapter_physicaldbname=au_adapter_physicaldbname,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_urlstring=dev_adapter_urlstring,
        dev_adapter_batchsize=dev_adapter_batchsize,
        dev_adapter_physicaldbname=dev_adapter_physicaldbname,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_urlstring=pro_adapter_urlstring,
        pro_adapter_batchsize=pro_adapter_batchsize,
        pro_adapter_physicaldbname=pro_adapter_physicaldbname
    )
    return output


def generated_salesforce_pe(uuaa_master=None, country=None, process_name=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('saleforce.html')
    title_html = "SALEFORCEPERU - salesforce.pe"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_loginurl = ""
    au_adapter_apiversion = f""

    dev_adapter_id = f"adapter-saleforcepe{process_name.lower()}-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-saleforcepe{process_name.lower()}-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter SALESFORCE in UUAA {uuaa_master.upper()} saleforcepe{process_name.lower()} files in dev"
    dev_adapter_loginurl = ""
    dev_adapter_apiversion = f""

    pro_adapter_id = f"adapter-saleforcepe{process_name.lower()}-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-saleforcepe{process_name.lower()}-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter SALESFORCE in UUAA {uuaa_master.upper()} saleforcepe{process_name.lower()} files in pro"
    pro_adapter_loginurl = ""
    pro_adapter_apiversion = f""

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_loginurl=au_adapter_loginurl,
        au_adapter_apiversion=au_adapter_apiversion,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_loginurl=dev_adapter_loginurl,
        dev_adapter_apiversion=dev_adapter_apiversion,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_loginurl=pro_adapter_loginurl,
        pro_adapter_apiversion=pro_adapter_apiversion
    )
    return output


def generated_sftp_eglobal(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('sftp.html')
    title_html = "SFTP Eglobal - sftp.internal.password"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_basepath = ""
    au_adapter_host = f""
    au_adapter_hostkey = ""
    au_adapter_port = f""

    dev_adapter_id = f"adapter-sftpeglobal-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-sftpeglobal-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter SFTP in UUAA {uuaa_master.upper()} sftpeglobal files in dev"
    dev_adapter_basepath = "/home1/eglobal1"
    dev_adapter_host = f"118.250.228.51"
    dev_adapter_hostkey = ""
    dev_adapter_port = f"22"

    pro_adapter_id = f"adapter-sftpeglobal-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-sftpeglobal-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter SFTP in UUAA {uuaa_master.upper()} sftpeglobal files in pro"
    pro_adapter_basepath = "/home1/eglobal1"
    pro_adapter_host = f"118.250.228.51"
    pro_adapter_hostkey = ""
    pro_adapter_port = f"22"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_host=au_adapter_host,
        au_adapter_hostkey=au_adapter_hostkey,
        au_adapter_port=au_adapter_port,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_host=dev_adapter_host,
        dev_adapter_hostkey=dev_adapter_hostkey,
        dev_adapter_port=dev_adapter_port,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_host=pro_adapter_host,
        pro_adapter_hostkey=pro_adapter_hostkey,
        pro_adapter_port=pro_adapter_port,
    )
    return output


def generated_sftp_openpay(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('sftp.html')
    title_html = "SFTP OPENPAY - sftp.external.pubkey"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_basepath = ""
    au_adapter_host = f""
    au_adapter_hostkey = ""
    au_adapter_port = f""

    dev_adapter_id = f"adapter-sftpopenpay-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-sftpopenpay-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter SFTP in UUAA {uuaa_master.upper()} sftpopenpay files in dev"
    dev_adapter_basepath = "/"
    dev_adapter_host = f"c45085c51c4f4994a.openpay.mx"
    dev_adapter_hostkey = ""
    dev_adapter_port = f"22"

    pro_adapter_id = f"adapter-sftpopenpay-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-sftpopenpay-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter SFTP in UUAA {uuaa_master.upper()} sftpopenpay files in pro"
    pro_adapter_basepath = "/"
    pro_adapter_host = f"0e2110cf1f4547beb.openpay.mx"
    pro_adapter_hostkey = ""
    pro_adapter_port = f"22"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_host=au_adapter_host,
        au_adapter_hostkey=au_adapter_hostkey,
        au_adapter_port=au_adapter_port,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_host=dev_adapter_host,
        dev_adapter_hostkey=dev_adapter_hostkey,
        dev_adapter_port=dev_adapter_port,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_host=pro_adapter_host,
        pro_adapter_hostkey=pro_adapter_hostkey,
        pro_adapter_port=pro_adapter_port,
    )
    return output


def generated_sftp_custom(uuaa_master=None, country=None, process_name=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('sftp.html')
    title_html = f"SFTP {process_name.upper()}- sftp.internal.password or sftp.external.password"

    au_adapter_id = f""
    au_adapter_connection_id = f""
    au_adapter_desc = f""
    au_adapter_basepath = ""
    au_adapter_host = f""
    au_adapter_hostkey = ""
    au_adapter_port = f""

    dev_adapter_id = f"adapter-sftp{process_name.lower()}-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-sftp{process_name.lower()}-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter SFTP in UUAA {uuaa_master.upper()} sftp{process_name.lower()} files in dev"
    dev_adapter_basepath = ""
    dev_adapter_host = f""
    dev_adapter_hostkey = ""
    dev_adapter_port = f"22"

    pro_adapter_id = f"adapter-sftp{process_name.lower()}-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-sftp{process_name.lower()}-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter SFTP in UUAA {uuaa_master.upper()} sftp{process_name.lower()} files in pro"
    pro_adapter_basepath = ""
    pro_adapter_host = f""
    pro_adapter_hostkey = ""
    pro_adapter_port = f"22"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_host=au_adapter_host,
        au_adapter_hostkey=au_adapter_hostkey,
        au_adapter_port=au_adapter_port,
        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_host=dev_adapter_host,
        dev_adapter_hostkey=dev_adapter_hostkey,
        dev_adapter_port=dev_adapter_port,
        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_host=pro_adapter_host,
        pro_adapter_hostkey=pro_adapter_hostkey,
        pro_adapter_port=pro_adapter_port,
    )
    return output


def generated_bts(uuaa_master=None, country=None):
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('bts.html')
    title_html = "GCS - gcs.bbva"

    au_adapter_id = f"adapter-bts-{uuaa_master.lower()}-v0"
    au_adapter_connection_id = f"con-pe-adapter-bts-{uuaa_master.lower()}-au-v0"
    au_adapter_desc = f"Adapter BTS in UUAA {uuaa_master.upper()} in au"
    au_adapter_basepath = ""
    au_adapter_bucket = ""
    au_adapter_region = ""

    dev_adapter_id = f"adapter-bts-{uuaa_master.lower()}-v0"
    dev_adapter_connection_id = f"con-pe-adapter-bts-{uuaa_master.lower()}-dev-v0"
    dev_adapter_desc = f"Adapter BTS in UUAA {uuaa_master.upper()} in dev"
    dev_adapter_basepath = f"dev/{uuaa_master.lower()}"
    dev_adapter_bucket = "bts-work-02-pe-ap"
    dev_adapter_region = "mx-le-1"

    pro_adapter_id = f"adapter-bts-{uuaa_master.lower()}-v0"
    pro_adapter_connection_id = f"con-pe-adapter-bts-{uuaa_master.lower()}-pro-v0"
    pro_adapter_desc = f"Adapter BTS in UUAA {uuaa_master.upper()} in pro"
    pro_adapter_basepath = f"pro/{uuaa_master.lower()}"
    pro_adapter_bucket = "bts-live-02-pe-ap"
    pro_adapter_region = "mx-le-1"

    output = template.render(
        title_html=title_html,
        au_adapter_id=au_adapter_id,
        au_adapter_connection_id=au_adapter_connection_id,
        au_adapter_desc=au_adapter_desc,
        au_adapter_basepath=au_adapter_basepath,
        au_adapter_bucket=au_adapter_bucket,
        au_adapter_region=au_adapter_region,

        dev_adapter_id=dev_adapter_id,
        dev_adapter_connection_id=dev_adapter_connection_id,
        dev_adapter_desc=dev_adapter_desc,
        dev_adapter_basepath=dev_adapter_basepath,
        dev_adapter_bucket=dev_adapter_bucket,
        dev_adapter_region=dev_adapter_region,

        pro_adapter_id=pro_adapter_id,
        pro_adapter_connection_id=pro_adapter_connection_id,
        pro_adapter_desc=pro_adapter_desc,
        pro_adapter_basepath=pro_adapter_basepath,
        pro_adapter_bucket=pro_adapter_bucket,
        pro_adapter_region=pro_adapter_region
    )
    return output


def generated_structure_ticket():
    from spark_dataframe_tools import get_color_b
    ticket = get_color_b(
        """
       ----
       Se solicita la creación del adaptador en DataX
    
       {color:#0747a6}*UUAA:*{color}  {key_uuaa}
       {color:#0747a6}*NS:*{color}  {key_ns}
       * {color:#0747a6}*Adapter ID:*{color}  {key_adapter_id}
       * {color:#0747a6}*Connection ID:*{color}   {key_connection_id}
       * {color:#0747a6}*Adapter description:*{color}  {key_adapter_description}
       * {color:#0747a6}*Datos de conexión:*{color}
       ** {color:#0747a6}*BasePath:*{color}  {key_basepath}
       ** {color:#0747a6}*Tenant:*{color}  {key_tenant}
    
       ----
       """)
    return ticket


adapter_input_dropdown = widgets.Dropdown(
    options=[('--Seleccione --', ""),
             ("Hdfs", "hdfs"),
             ("OraclePe", "oracle"),
             ("OracleCustom", "oracle"),
             ("Launchpad", "gcs"),
             ("saleforce", "saleforce"),
             ("connectdirect", "connectdirect"),
             ("host", "host"),
             ("AWS Bucket", "awsbucket"),
             ("GCP Bucket", "gcsbucket"),
             ("Sftp", "sftp"),
             ("Elasticsearch", "elasticsearch"),
             ("Coredocument", "coredocument"),
             ("Bts", "bts"),
             ],
    value='',
    disabled=False,
    description='Adap. Orig:'
)
adapter_output_dropdown = widgets.Dropdown(
    options=[('--Seleccione --', ""),
             ("Hdfs", "hdfs"),
             ("OraclePe", "oracle"),
             ("OracleCustom", "oracle"),
             ("Launchpad", "gcs"),
             ("saleforce", "saleforce"),
             ("connectdirect", "connectdirect"),
             ("host", "host"),
             ("AWS Bucket", "awsbucket"),
             ("GCP Bucket", "gcsbucket"),
             ("Sftp", "sftp"),
             ("Elasticsearch", "elasticsearch"),
             ("Coredocument", "coredocument"),
             ("Bts", "bts"),
             ],
    value='',
    description='Adap. Dest:',
    disabled=False
)
text_table_name = widgets.Text(
    value='',
    placeholder='Table Name',
    description='Table Name:',
    disabled=False
)

button_generated_momenclature = widgets.Button(
    description='Generate Momenclature',
    disabled=False,
    button_style='primary'
)
result_adapter_momenclature = widgets.HTML(value="")
out2 = widgets.Output()
box_button_generated_momenclature = widgets.VBox(
    [
        adapter_input_dropdown,
        adapter_output_dropdown,
        text_table_name,
        button_generated_momenclature,
        result_adapter_momenclature
    ]
)


def load_select_adapter_momenclature():
    display(box_button_generated_momenclature)
    display(out2)


def evaluate_adapter_generated_momenclature(_):
    out2.clear_output()
    if adapter_input_dropdown.value == "":
        result_adapter_momenclature.value = "<b>Required Input</b>"
    elif adapter_output_dropdown.value == "":
        result_adapter_momenclature.value = "<b>Required Output</b>"
    elif text_table_name.value == "":
        result_adapter_momenclature.value = "<b>Required TableName</b>"
    else:
        with out2:
            rs = datax_generated_nomenclature(table_name=text_table_name.value,
                                              origen=adapter_input_dropdown.value,
                                              destination=adapter_output_dropdown.value)
            result_adapter_momenclature.value = rs
            adapter_input_dropdown.value = ""
            adapter_output_dropdown.value = ""
            text_table_name.value = ""


button_generated_momenclature.on_click(evaluate_adapter_generated_momenclature)


def datax_generated_nomenclature(table_name, origen, destination, output=True):
    """
    Create the datax nomenclatures
    :param table_name: String
    :param origen: String
    :param destination: String
    :param output: Boolean
    :return:
    """
    from jinja2 import Environment, FileSystemLoader
    from spark_datax_tools import BASE_DIR
    import os
    import sys

    if table_name in ("", None):
        raise Exception(f'required variable table_name')
    if origen in ("", None):
        raise Exception(f'required variable origen')
    if destination in ("", None):
        raise Exception(f'required variable destination')
    if output in ("", None):
        raise Exception(f'required variable output value True or False')

    uuaa = str(str(table_name).lower().split("_")[1])
    table_short = "".join(table_name.split("_")[2:])
    is_windows = sys.platform.startswith('win')
    templates_dir = os.path.join(BASE_DIR, "utils", "files")
    if is_windows:
        templates_dir = templates_dir.replace("\\", "/")

    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True
    template = env.get_template('datax.html')
    title_html = "DATAX MOMENCLATURE"

    transfer_id = "p{uuaa}_{origen}{destination}{table_short}_0".format(
        uuaa=uuaa, origen=origen, destination=destination, table_short=table_short)
    schema_in_id = "x_schema_{origen}{table_short}_in_0".format(
        origen=origen, table_short=table_short)
    schema_out_id = "x_schema_{destination}{table_short}_out_0".format(
        destination=destination, table_short=table_short)
    do_read_id = "x_read{origen}{table_short}_0".format(
        origen=origen, table_short=table_short)
    do_write_id = "x_write{destination}{table_short}_0".format(
        destination=destination, table_short=table_short)

    output = template.render(
        title_html=title_html,
        transfer_id=transfer_id,
        do_read_id=do_read_id,
        do_write_id=do_write_id,
        schema_in_id=schema_in_id,
        schema_out_id=schema_out_id
    )

    return output


def datax_generated_schema_artifactory(path_json=None,
                                       is_schema_origen_in=True,
                                       schema_type=None,
                                       convert_string=False,
                                       env=None):
    """
    Generated schema artifactory
    :param path_json: String
    :param is_schema_origen_in: Boolean
    :param schema_type: String
    :param convert_string: Boolean
    :param env: String
    :return:
    """
    import json
    import os
    from spark_dataframe_tools import spark_reformat_dtype_data
    from spark_dataframe_tools import get_color_b

    if path_json in ("", None):
        raise Exception(f'required variable path_json')
    if is_schema_origen_in in ("", None):
        raise Exception(f'required variable is_schema_origen_in value is True or False')
    if schema_type in ("", None):
        raise Exception(f'required variable schema_type value is hdfs,host,gcs,xcom')
    if convert_string in ("", None):
        raise Exception(f'required variable convert_string value is hdfs,host,gcs,xcom')

    schema_type = str(schema_type).lower()

    dataset_json = path_json
    with open(dataset_json) as f:
        datax = json.load(f)
    table_name = table = datax.get("name", "")
    uuaa = str(table_name.split("_")[1]).upper().strip()
    table_short = "".join(table_name.split("_")[2:])
    description = datax.get("description", "")

    if is_schema_origen_in:
        schema_name = "x_schema_{schema_type}{table_short}_in_0".format(
            schema_type=schema_type, table_short=table_short)
    else:
        schema_name = "x_schema_{schema_type}{table_short}_out_0".format(
            schema_type=schema_type, table_short=table_short)

    rs_dict = dict()
    for field in datax["fields"]:
        if str(env).lower() == "work":
            naming = field.get("legacyName", "")
        else:
            naming = field.get("name", "")
        _format = field.get("logicalFormat", "")
        reformat_data = spark_reformat_dtype_data(
            columns=naming, format=_format, convert_string=convert_string)
        _format = reformat_data["_format"]
        _mask = reformat_data["_mask"]
        _locale = reformat_data["_locale"]
        _type = reformat_data["_type"]
        _schema_type = reformat_data["_schema_type"]

        if table not in rs_dict.keys():
            rs_dict[table] = dict(_id="", description="", fields=list())
        rs_dict[table]["_id"] = schema_name
        rs_dict[table]["description"] = description
        fields_dict = dict()
        fields_dict["name"] = naming
        fields_dict["logicalFormat"] = _format
        fields_dict["deleted"] = False
        fields_dict["metadata"] = False
        fields_dict["default"] = ""
        fields_dict["mask"] = _mask
        fields_dict["locale"] = _locale
        fields_dict["mandatory"] = False
        rs_dict[table]["fields"].append(fields_dict)

    path_directory = os.path.join('schema_artifactory', uuaa, table_name)
    path_filename = os.path.join(path_directory, f"{schema_name}.json")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    with open(path_filename, 'w') as f:
        json.dump(rs_dict[f"{table_name}"], f, indent=4)
    print(get_color_b(f'GENERATED SCHEMA: {table_name}'))
    print(f'create file for schema: {schema_name}.json')
