# /usr/bin/env python
# coding=utf-8

html_template = """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>CDNX  Scan Report</title>
	<style text="">
		body{
			width: 80%;
			margin:auto
		}
		h3{
			padding-left: 5%;
		}
		div{
			padding-left: 5%;
		}
		ul li{
			list-style-type: disc;
		}
		p{
			text-indent: 2em;
		}
		.ip{
			line-height: 25px;
			padding-top: 5px;
			margin-top: 10px;
		}


	</style>
</head>
<body>
	<h3>域名{domain}扫描结果</h3>
	<div>
		<ol>
            {content_template}
		</ol>
	</div>

</body>
</html>
"""

content_template = """
<li class="ip">IP:{ip}</li>

<ul>
    <li>Status:{status}</li>
    <li>Server:{server}</li>
    <li>X_Powered_By:{x_powered_by}</li>
    <li><a target="_blank" href="{href}">Content</a></li>
</ul>
"""