<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="${request.static_url('angerona2:static/mfc.png')}">

    <title>Jumbotron Template for Bootstrap</title>
    
    <link href="${request.static_url('angerona2:static/css/bootstrap.min.css')}" rel="stylesheet">
    <link href="${request.static_url('angerona2:static/css/styles.css')}" rel="stylesheet">
    
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <!-- / AddedCSS / -->
    <%block name="AddedCSS"/>
</head>
<body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <ul class="nav navbar-nav">

% for item in vc.navmenu:
<%
                if item['active'] == 1:
                    active = 'active'
                else:
                    active = ''

%>              <li role="presentation" class="${active}"><a href="${item['url']}">${item['txt']}</a></li>
% endfor
            </ul>
        </div>
    </nav>

	<div class="container">
        <!-- / BlockContent / -->
        <%block name="BlockContent"/>
        <!-- / BlockContent / -->
	</div>

	<footer>
		<p></p>
        <div class="container">
            <p>&copy; Nextraztus 2015</p>
        </div>
    </footer>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="${request.static_url('angerona2:static/js/bootstrap.min.js')}"></script>

    <!-- / AddedJS / -->
    <%block name="AddedJS"/>

</body>
</html>