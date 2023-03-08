import numpy as np



def create_output(bearing):

    htmlcontent = """
    <!DOCTYPE HTML>
    <HTML><HEAD><META content="IE=11.0000" http-equiv="X-UA-Compatible">

    <META name="author" content="Romax" technology=""> 
    <META charset="UTF-8"> 
    <META http-equiv="X-UA-Compatible" content="IE=Edge,10,9,8,7"> 
    <STYLE type="text/css">/*Romax Report*/
    td,th,body {font-family: sans-serif; font-size: 12px; color: #000000}
    br {clear: all;}
    caption { text-align: left; font-weight: bold; font-size: 12px; }
    hr {page-break-after: always}
    table {margin-bottom: 20; border-collapse: collapse; border: 1px solid black}
    td { text-align: center}
    tr { height: 20px; }
    tr:nth-child(even) {background-color: #f2f2f2;}
    /* tr:hover {background: yellow;} */
    body {
        background-repeat: no-repeat;
        margin-top: 70px; 
    }
    * {
        box-sizing: border-box;
        }
    /* Create two equal columns that floats next to each other */
    .column {
        float: left;
        width: 50%;

    }

    /* Clear floats after the columns */
    .row:after {
        content: "";
        display: table;
        clear: both;
    }
    </STYLE>
    
    <META name="GENERATOR" content="MSHTML 11.00.10570.1001"></HEAD>
    <BODY>"""

    htmlcontent += "<H2>Life - 16281 - Summary</H2>"

    htmlcontent += """
    <DIV>
    <TABLE border="3" cellspacing="1" cellpadding="1">
    <TBODY>
    <TR>
        <TD rowspan="1" colspan="2">
        <DIV>Reference Life(MRev)</DIV></TD>
        <TD rowspan="1" colspan="2">
        <DIV>{:4e}</DIV></TD>
    </TR>
    <TR>
        <TD rowspan="1" colspan="2">
        <DIV>Equivalent Radial Load(N)</DIV></TD>
        <TD rowspan="1" colspan="2">
        <DIV>{}</DIV></TD>
    </TR>
    <TR>
        <TD rowspan="1" colspan="2">
        <DIV>Load Zone Factor</DIV></TD>
        <TD rowspan="1" colspan="2">
        <DIV>{}</DIV></TD>
    </TR>
    </TBODY>
    </TABLE>
    </DIV>

    """.format(bearing.reference_life, bearing.radial_load, bearing.load_zone)



    # ======== Roller Loads ==========

    htmlcontent += "<br/><br/><H2>Roller Loads and Deflections</H2>"
    htmlcontent += """
    <DIV>
    <TABLE border="3" cellspacing="1" cellpadding="1">
    <TBODY>
    <TR>
        <TH>
        <DIV>Angular Position (deg)</DIV></TH>
        <TH>
        <DIV>Roller Loads(N)</DIV></TH>
        <TH>
        <DIV>Roller deflections(um)</DIV></TH>
    </TR>
    """

    for item in range(bearing.num_rollers):
        htmlcontent += """
                            <TR>
                                <TD>
                                <DIV>{}</DIV></TD>
                                <TD>
                                <DIV>{}</DIV></TD>
                                <TD>
                                <DIV>{}</DIV></TD>
                            </TR>""".format(round(bearing.roller_model['roller_positions'][item], 2), 
                                            round(bearing.roller_model['roller_loads'][item], 2),
                                            round(bearing.roller_model['roller_deflections'][item] * 1000, 2))
    htmlcontent += """</TBODY></TABLE></DIV>"""
    htmlcontent += """<br/>
    <DIV>
        <H4>Roller Load Distribution</H4>
        <DIV><IMG align="absmiddle" src=""> Aligned to make highest loaded roller takes zero position
            <P><IMG alt="Raceway load against circumferential position (N)" src="outfig/Roller_loads.png" border="2"> </P>
        </DIV>
    </DIV> 
    """
    

    
    # ======== Contact Stress ==========
    htmlcontent += "<br/><br/><H2>Roller Contact Stresses</H2>"
    htmlcontent += """
    <DIV>
        <H4>Roller Contact Stresses</H4>
        <DIV><IMG align="absmiddle" src=""> Aligned to make highest loaded roller takes zero position
            <P><IMG alt="Raceway load against circumferential position (N)" src="outfig/Contact_Stress.png" border="2"> </P>
        </DIV>
    </DIV> 
    """
    htmlcontent += """<br/>
    <DIV>
    <TABLE border="3" cellspacing="1" cellpadding="1">
    <TBODY>
    <TR>
        <TH>
        <DIV>Angular Position (deg)</DIV></TH>
        <TH>
        <DIV>Roller Position from center(mm)</DIV></TH>
        <TH>
        <DIV>Inner Raceway Max Contact Pressure(Mpa)</DIV></TH>
        <TH>
        <DIV>Inner Raceway semi-width(um)</DIV></TH>
        <TH>
        <DIV>Outer Raceway Max Contact Pressure(Mpa)</DIV></TH>
        <TH>
        <DIV>Outer Raceway semi-width(um)</DIV></TH>
    </TR>
    """

    for i in range(bearing.num_rollers):
        if not(np.isnan(bearing.bearing_model['contact_stresses_inner_array'][i,:]).all()):
            for j in range(bearing.num_laminas):
                # max_inner_stress = max(bearing.bearing_model['contact_stresses_inner_array'][item])
                # max_inner_stress_index = (np.where(bearing.bearing_model['contact_stresses_inner_array'][item] == max_inner_stress))[0]
                # max_outer_stress = max(bearing.bearing_model['contact_stresses_outer_array'][item])
                # max_outer_stress_index = (np.where(bearing.bearing_model['contact_stresses_outer_array'][item] == max_outer_stress))[0]
                htmlcontent += """
                                <TR>
                                    <TD>
                                    <DIV>{}</DIV></TD>
                                    <TD>
                                    <DIV>{}</DIV></TD>
                                    <TD>
                                    <DIV>{}</DIV></TD>
                                    <TD>
                                    <DIV>{}</DIV></TD>
                                    <TD>
                                    <DIV>{}</DIV></TD>
                                    <TD>
                                    <DIV>{}</DIV></TD>
                                </TR>""".format(round(bearing.roller_model['roller_positions'][i], 2), 
                                                round(bearing.lamina_model['lamina_positions'][j], 2),
                                                round(bearing.bearing_model['contact_stresses_inner_array'][i][j], 2),
                                                round(bearing.bearing_model['semi_width_inner_array'][i][j] * 1000, 2),
                                                round(bearing.bearing_model['contact_stresses_outer_array'][i][j], 2),
                                                round(bearing.bearing_model['semi_width_outer_array'][i][j] * 1000, 2))
    htmlcontent += """</TBODY></TABLE></DIV>"""
    
    # ======== Profile Data ==========
    htmlcontent += "<br/><br/><H2>Profile Data</H2>"
    htmlcontent += """
    <DIV>
        <H4>Roller profile</H4>
        <DIV>
            <P><IMG alt="Raceway load against circumferential position (N)" src="outfig/Profile.png" border="2"> </P>
        </DIV>
    </DIV> 
    """

    htmlcontent += """<br/>
    <DIV>
    <TABLE border="3" cellspacing="1" cellpadding="1">
    <TBODY>
    <TR>
        <TH>
        <DIV>Roller Position(mm)</DIV></TH>
        <TH>
        <DIV>Profile(um)</DIV></TH>
    </TR>
    """

    for i in range(bearing.num_laminas):
        htmlcontent += """
                            <TR>
                                <TD>
                                <DIV>{}</DIV></TD>
                                <TD>
                                <DIV>{}</DIV></TD>
                                
                            </TR>""".format( 
                                            round(bearing.lamina_model['lamina_positions'][i], 2),
                                            round(bearing.profile_data[i] * 1000, 2),
                                            )
                        
    htmlcontent += """</TBODY></TABLE></DIV>"""


    hs = open("asciiCharHTMLTable.html", 'w')
    hs.write(htmlcontent)
    hs.close()