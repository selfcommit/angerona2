<%inherit file="angerona2:templates/base.mako" />
<%block name="BlockContent">

<form method="POST" id="dataform" enctype="multipart/form-data" accept-charset="utf-8"
	role="form" action="${request.route_url('secret')}">

<div class="row">
	<div class="col-md-6">
		<h3>Angerona</h3>
		<p>Set your maximum views, hours for the link to survive, the type of
		snippet. Input what to save in the "Data" field, click the button and you will
		be presented with a link you can paste to your intended recipient. This link
		will decrypt and display the data for them. After the configured self-destruct
		time elapses or number of views is reached, the data is removed from our
		database.</p>
		<p>Recipients with the link may choose to delete the data earlier.</p>
	</div>

	<div class="col-md-6">
		<div class="form-horizontal">
			<div class="form-group">&nbsp;</div>
			<div class="form-group">
				<label for="views_max" class="col-sm-4 control-label">Maximum Views </label>
				<div class="col-sm-8">
					<select name="maximum_views" id="maximum_views" class="form-control">
						<option value="-1">Unlimited Views</option>
						<option value="">- Number Total -</option>
						<option value="1">1</option>
						<option selected="selected" value="2">2</option>
						<option value="3">3</option>
						<option value="5">5</option>
						<option value="7">7</option>
						<option value="11">11</option>
						<option value="13">13</option>
						<option value="100">100</option>
					</select>
				</div>
			</div>

			<div class="form-group">
				<label for="hours_until_expiration" class="col-sm-4 control-label">Time Until Expiration </label>
				<div class="col-sm-8">
					<select name="hours_until_expiration" id="hours_until_expiration" class="form-control">
						<option value="">- Hours/Days -</option>
						<option value="1">1h</option>
						<option value="2">2h</option>
						<option selected="selected" value="4">4h</option>
						<option value="8">8h</option>
						<option value="12">12h</option>
						<option value="16">16h</option>
						<option value="20">20h</option>
						<option value="24">1d</option>
						<option value="36">1d 12h</option>
						<option value="48">2d</option>
						<option value="60">2d 12h</option>
						<option value="72">3d</option>
						<option value="84">3d 12h</option>
						<option value="96">4d</option>
						<option value="108">4d 12h</option>
						<option value="120">5d</option>
						<option value="144">6d</option>
						<option value="168">1w</option>
					</select>
				</div>
			</div>

			<div class="form-group">
				<label for="snippet_type" class="col-sm-4 control-label">Snippet Type </label>
				<div class="col-sm-8">
					<select name="snippet_type" id="snippet_type" class="form-control">
						<option selected="selected" value="">Password / Unformatted</option>
						<option value="as3">ActionScript3</option>
						<option value="shell">Bash/Shell</option>
						<option value="cf">ColdFusion</option>
						<option value="csharp">C#</option>
						<option value="cpp">C/C++</option>
						<option value="css">CSS</option>
						<option value="delphi">Delphi, Pascal</option>
						<option value="diff">Diff/Patch</option>
						<option value="erl">Erlang</option>
						<option value="groovy">Groovy</option>
						<option value="js">JavaScript</option>
						<option value="java">Java</option>
						<option value="jfx">JavaFX</option>
						<option value="pl">Perl</option>
						<option value="php">PHP</option>
						<option value="plain">Plain Text</option>
						<option value="ps">PowerShell</option>
						<option value="py">Python</option>
						<option value="ruby">Ruby</option>
						<option value="scala">Scala</option>
						<option value="sql">SQL</option>
						<option value="vb">Visual Basic</option>
						<option value="xml">XML,HTML,XML,XSLT</option>
					</select>
				</div>
			</div>

			<div class="checkbox">
				<span class="col-sm-4 control-label"></span>
				<div class="col-sm-8">
					<label>
						<input type="checkbox" name="disallow_early_delete" />
							No Early Delete
					</label>
				</div>
			</div>
		</div>
	</div>
</div>

<div class="row">&nbsp;</div>

<div class="row">
  <label for="Field4">Data</label>
  <textarea id="ta_data" name="data" rows="20" class="form-control"></textarea>
</div>

<div class="row">&nbsp;</div>

<div class="row">
  <button id="submit" name="submit" type="submit" class="submit btn btn-default" value="submit">
	  <span>Save, Encrypt &amp; Retrieve Link</span>
  </button>
</div>
</form>

</%block>