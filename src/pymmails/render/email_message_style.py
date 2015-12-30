"""
@file
@brief HTML style to display an Email
"""

template_email_css = """
.dataframe100l {
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

.dataframe100l_hl td {
    background: #FFFF00;
    }

.dataframe100l_hl th {
    background: #FFFF00;
    }

.dataframe100l_hl tr {
    background: #FFFF00;
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
"""

template_email_html = """<?xml version="1.0" encoding="utf-8"?>
<body>
<html>
<head>
<title>{{ message.get_field("subject") }}</title>
<link rel="stylesheet" type="text/css" href="{{ css }}">
</head>
<body>
{{ '<a href="{0}">&lt;--</a>'.format(prev_mail) if prev_mail else '' }}
{{ '<a href="{0}">--&gt;</a>'.format(next_mail) if next_mail else '' }}
<h1>{{ message.get_date().strftime('%Y/%M/%d') }} - {{ message.get_field("subject") }}</h1>
<h2>attributes</h2>
{{ render.produce_table_html(message, toshow=EmailMessage.subset, location=location, avoid=EmailMessage.avoid) }}
<h2>message</h2>
{{ render.process_body_html(location, message.body_html, attachments) }}
<h2>full list of attributes</h2>
{{ render.produce_table_html(message, toshow=message.Fields, location=location, tohighlight=EmailMessage.subset) }}
</body>
</html>
"""

template_email_list_html_begin = """<?xml version="1.0" encoding="utf-8"?>
<body>
<html>
<head>
<title>{{ title }}</title>
<link rel="stylesheet" type="text/css" href="{{ css }}">
</head>
<body>
<h1>{{ now.strftime('%Y/%M/%d') }} - {{ title }}</h1>
<ul>
"""

template_email_list_html_end = """
</ul>
</body>
</html>
"""

template_email_list_html_iter = """
<li><a href="{{ url }}">{{ message.get_date().strftime('%Y/%M/%d') }} - {{ message.get_from_str() }}</a> to {{ message.get_to_str() }} - {{ message.get_field("subject") }}</li>
"""
