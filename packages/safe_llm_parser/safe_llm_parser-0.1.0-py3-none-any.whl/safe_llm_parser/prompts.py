from textwrap import dedent


def create_fix_xml_prompt(xml_to_fix: str) -> str:
    return dedent(f"""# Context
                  You are an expert in XML parsing. 
                  You are given an XML string that is not valid.
                  You must fix the XML string so that it is valid XML, but you must not add new tags or entries.
                  It means you must correct only tags coherence, but not consistency.
                  You must also remove any string that would not be within tags, like "..." refering to potential addiotional information.
                  
                  # XML to fix
                  {xml_to_fix}
                                    
                  # Fixed XML
                  
                  Note: Remember not to check consistency, so do not create and add information to the corrected XML.
                  
                  """)
