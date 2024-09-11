import os
from datetime import datetime
from ..crystalpy_barno import *

# Set database connection details externally
DatabaseConnectionHelper.set_connection_details(
    server_name="NjmsReport",
    database_name="Nishka",
    user_id="sa",
    password="nimbus@123"
)
# Get the current working directory
cwd_ = os.getcwd()

# Define the path to the configuration file
config_path = os.path.join(cwd_, 'tests/config.json')

# # Create an instance of the CrystalReportsLoader class
# loader = CrystalReportsLoader()

# # Setup the loader (loads config, DLLs, and namespaces)
# loader.setup()

voucher_no = "2425SOPDKNB0158"
pdf_dir = os.path.join(cwd_, 'pdf')
pdf_dir_sales = os.path.join(pdf_dir, 'sales')
pdf_filepath_sale = os.path.join(pdf_dir_sales, f"{voucher_no}.pdf")
pdf_dir = os.path.join(cwd_, 'pdf')
pdf_dir_reports = os.path.join(pdf_dir, 'reports')
pdf_filepath_stock = os.path.join(pdf_dir_reports, f"Stock_Report.pdf")

if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

if not os.path.exists(pdf_dir_sales):
    os.makedirs(pdf_dir_sales)

if not os.path.exists(pdf_dir_reports):
    os.makedirs(pdf_dir_reports)

params = {
    "source_no": "2425SOEDKNB1981",
    "voucher_no": voucher_no,
    "le_code": "AJPL",
    "user_code": "NIM",
    "s_inc_mak": True,
    "s_emp_name": "emp_name_value",
    "le_name": "le_name_value",
    "wh_name": "wh_name_value",
    "wh1": "wh1_value",
    "wh2": "wh2_value",
    "whp1": "whp1_value",
    "whp2": "whp2_value",
    "s_print_hdr": True,
}

SaleSnippet.SaleMemo(
    report_filename=os.path.join(cwd_, 'tests/rpt/Sale_Memo_IncludeMaking.rpt'),
    output_path=pdf_filepath_sale,
    params=params,
    report_type = 1
)
