import xml.etree.ElementTree as ET

# 주어진 문자열
country_data_as_string = r"""<Sequence sap2010:WorkflowViewState.IdRef=\"Sequence_3\">
      <bn:OpenURL Browser=\"{x:Null}\" NewTab=\"{x:Null}\" UserDataFolderMode=\"{x:Null}\" UserDataFolderPath=\"{x:Null}\" sap2010:WorkflowViewState.IdRef=\"OpenBrowser_1\" Url=\"http://naver.com\" />
      <Sequence sap2010:WorkflowViewState.IdRef=\"Sequence_2\">
      </Sequence>
    </Sequence>"""

# XML 요소로 파싱
root = ET.fromstring(country_data_as_string)
print(root)

xml_data = "<root>...</root>"
# print(ET.canonicalize(country_data_as_string))
# for ele in root:
    
