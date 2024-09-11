import os
from crystalpy_barno.ReportsClasses.Base_Report import *
from crystalpy_barno.ReportsClasses.Helper.database_helper import DatabaseConnectionHelper
from crystalpy_barno.ReportsClasses.Base_Report import CrystalReportsLoader

# Create an instance of the CrystalReportsLoader class
loader = CrystalReportsLoader()

# Setup the loader (loads config, DLLs, and namespaces)
loader.setup()

import CrystalDecisions.CrystalReports.Engine as Engine
from CrystalDecisions.Windows import Forms
from CrystalDecisions import Shared
from CrystalDecisions.CrystalReports.Engine import ReportDocument
from CrystalDecisions.Shared import ParameterDiscreteValue, TableLogOnInfo, ExportFormatType

class StockSnippet:
    @staticmethod
    def SummaryClosing(report_filename, output_path, params):
        crpt = Engine.ReportDocument()
        crpt.Load(report_filename)
        cr_viewer = Forms.CrystalReportViewer()

        def set_parameter(param_name, value):
            cr_param = ParameterDiscreteValue()
            cr_param.Value = value
            crpt.DataDefinition.ParameterFields[param_name].CurrentValues.Clear()
            crpt.DataDefinition.ParameterFields[param_name].CurrentValues.Add(cr_param)
            crpt.DataDefinition.ParameterFields[param_name].ApplyCurrentValues(crpt.DataDefinition.ParameterFields[param_name].CurrentValues)

        # Setting Parameters using values from the dictionary
        set_parameter("@pvReportId", "4")
        set_parameter("@pvFromDate", params.get('s_from_date'))
        set_parameter("@pvToDate", params.get('s_to_date'))
        set_parameter("@pvProduct", params.get('s_product'))
        set_parameter("@pvCheck", params.get('s_check'))
        set_parameter("@pvPurity", params.get('s_purity'))
        set_parameter("@pvSize", params.get('s_size'))
        set_parameter("@pvCut", params.get('s_cut'))
        set_parameter("@pvColor", params.get('s_color'))
        set_parameter("@pvStyle", params.get('s_style'))
        set_parameter("@pvBatch", params.get('s_batch'))
        set_parameter("@pvLeCode", params.get('s_le_code'))
        set_parameter("@pvWH", params.get('s_wh'))
        set_parameter("@pvArticle", params.get('s_article'))
        set_parameter("@pvCompl", params.get('s_compl'))
        set_parameter("@pvMNF", params.get('s_mnf'))
        set_parameter("@pvHierarchy", params.get('s_hierarchy'))
        set_parameter("@pvOnlySKUType", params.get('s_sku_type'))
        set_parameter("@pvExCludeOld", params.get('s_ex_old'))
        set_parameter("@pvStockType", params.get('s_bk_type'))
        set_parameter("@pvOnlyIssue", "0")
        set_parameter("@pvUser", params.get('s_user'))
        set_parameter("@pvRepair", params.get('s_repair'))
        set_parameter("@pvDepartment", params.get('s_department'))

        # Apply database connection using the centralized helper
        DatabaseConnectionHelper.apply_connection(crpt)

        crpt.Database.Tables[0].Location = f"{DatabaseConnectionHelper.get_database_name()}.dbo.spReports_ItemLedger"

        # Set formula fields
        formula_fields = crpt.DataDefinition.FormulaFields
        for field in formula_fields:
            if field.Name == "CompanyName":
                field.Text = f"'{params.get('cn')}'"
            elif field.Name == "Address1":
                field.Text = f"'{params.get('add')} - {params.get('city')}'"
            elif field.Name == "Address2":
                field.Text = f"'{params.get('coun')}'"

        # Set the Report Caption formula field based on warehouse status
        if params.get('s_wh'):
            report_caption = f"Item Ledger Closing Summary Of Warehouse: {params.get('s_whn')} From {params.get('s_from_date_formula')} To {params.get('s_to_date_formula')}"
        else:
            report_caption = f"Item Ledger Closing Summary Of Warehouse:(All) From {params.get('s_from_date_formula')} To {params.get('s_to_date_formula')}"

        crpt.DataDefinition.FormulaFields["ReportCaption"].Text = f"'{report_caption}'"

        # Export the report to the disk
        crpt.ExportToDisk(Shared.ExportFormatType.PortableDocFormat, output_path)

        # Set and show the report in the viewer
        cr_viewer.ReportSource = crpt
        cr_viewer.Refresh()
        cr_viewer.Show()

        return True

