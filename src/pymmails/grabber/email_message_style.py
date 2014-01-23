# coding: latin-1
"""
@file
@brief HTML style to display an Email
"""

html_header_style = """<?xml version="1.0" encoding="utf-8"?>
        <body>
        <html>
        <head>
        <title>__TITLE__</title>
        <style>
        
        .bodymail {
            // __MORE_STYLE1__
            margin-top:1%;
            margin-left:20%;
            margin-right:5%;
            padding: 0;
            width=75%
            font-family: Calibri;
            font-size: 100%;
            cursor: pointer;
        }             

        .dataframe100l {
            // __MORE_STYLE2__
            margin-top:1%;
            margin-left:20%;
            margin-right:5%;
            padding: 0;
            width=75%
            font-family: Calibri;
            font-size: 100%;
            cursor: pointer;
        }             

        .dataframe100l table { 
            border-collapse: collapse; 
            text-align: left; 
            font-size: 11px;
        } 

        .dataframe100l table td, .dataframe100l table th { 
            padding: 3px 6px; 
        }

        .dataframe100l table thead th {
            background-color:#AAAAAA; 
            color:#ffffff; 
            font-size: 11px; 
            font-weight: bold; 
            border-left: 1px solid #0070A8; 
        } 

        .dataframe100l table tbody td { 
            color: #00496B; 
            border-left: 1px solid #E1EEF4;
            font-size: 11px;
            font-weight: normal; 
        }

        .dataframe100l table tbody .alt td { 
            background: #E1EEF4; 
            color: #00496B; 
            }
            
        .dataframe100l table tbody td:first-child { 
            border-left: none; 
        }

        .dataframe100l table tbody tr:last-child td { 
            border-bottom: none; 
        }

        .dataframe100l table tfoot td div { 
            border-top: 1px solid #006699;
            background: #E1EEF4;
        } 

        .dataframe100l table tfoot td { 
            padding: 0; 
            font-size: 11px 
        } 

        .dataframe100l table tfoot td div{ padding: 2px; }
        .dataframe100l table tfoot td ul { 
            margin: 0; 
            padding:0; 
            list-style: none; 
            text-align: right; 
        }

        .dataframe100l table tfoot  li { display: inline; }
        .dataframe100l table tfoot li a { 
            text-decoration: none; 
            display: inline-block;  
            padding: 2px 8px; 
            margin: 1px;
            color: #FFFFFF;
            border: 1px solid #006699;
            border-radius: 3px; 
            background-color:#006699; 
        }

        .dataframe100l table tfoot ul.active, .dataframe100l table tfoot ul a:hover { 
            text-decoration: none;
            border-color: #006699; 
            color: #FFFFFF; 
            background: none; 
            background-color:#00557F;
        }            
        </style>
        </head>
        <body>
        <!-- NAVIGATION -->
        """.replace("        ","")
