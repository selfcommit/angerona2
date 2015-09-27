<%inherit file="angerona2:templates/base.mako" />
<%block name="AddedJS">

<script type="text/javascript" src="${request.static_url('angerona2:static/js/holder.min.js')}"></script>
<script type="text/javascript">
    $('document').ready(function (){
        $('#snippet_type_table tbody:first').hide();
        $('#snippet_type_table thead:first').click(function() {
            $('#snippet_type_table tbody:first').slideToggle(400);
        });
    });
   
</script>

</%block>
<%block name="AddedCSS">

<style type="text/css">
    table#snippet_type_table thead { cursor: pointer; }

    .bg   { background-color: #000; }
    .resp { color: #9cd0ff; }
    .req  { color: #ffd09c; }
    .wh   { color: #c0c0c0; }

    .hlwh { background-color: #c0c0c0; }
    .hl2  { background-color: #fbffff; }
    .hl   { background-color: #f4fcff; }
</style>

</%block>
<%block name="BlockContent">

<div class="container">
    <div class="row hl">
        <div class="col-sm-2">
            <h3>Overview</h3>
        </div>
        <div class="col-sm-10">
            <h3>Standard Request/Response Object(s)</h3>
            <p>Our API utilizes HTTP verbs and HTTP response codes; all responses are encoded into a
            JSON object described by each documented function. UTF-8 is expected. HTTP response code
            will usually make sense with what's happening.</p>

            <pre class="bg resp">{'status': _int_, 'msg': _str_, 'data': _any_}</pre>

            <p>All methods are documented below.</p>

            <p>Generic/standard Error Responses</p>

        </div>
        <div class="clearfix"></div>
    </div>

    <div class="row hl2">
        <div class="col-sm-2">
            <h3>Secret(s)</h3>
        </div>
        <div class="col-sm-10">
            <h3>Create/Store</h3>
            <p>This method will create a secret to your specifications; the POST body will be the
            data that is stored and encrypted. UTF-8 encoding all around, the optional arguments
            below tweak the storage parameters.</p>
            <pre class="bg req">POST /api/v1/secret</pre>
            <h3>Optional Arguments</h3>
            <table class="table table-condensed">
                <tr><td>?maximum_views</td><td>expects int range:[1,100] default:2</td></tr>
                <tr><td>?maximum_hours</td><td>expects int range:[1,168] default:4</td></tr>
                <tr><td>?set_unlimited_views</td><td>expects bool default: off; preempts maximum_views</td></tr>
                <tr><td>?set_early_expire</td><td>expects bool default: on</td></tr>
                <tr><td>?set_snippet_type</td><td>defaults unformatted (empty string), expand table for values<br/>
                                                <table class="table table-condensed" id="snippet_type_table">
                                                    <thead>
                                                        <tr><th></th><th>+ Toggle Table +</th></tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr><td></td><td>Password / Unformatted (Default)</td></tr>
                                                        <tr><td>as3</td><td>ActionScript3</td></tr>
                                                        <tr><td>shell</td><td>Bash/Shell</td></tr>
                                                        <tr><td>cf</td><td>ColdFusion</td></tr>
                                                        <tr><td>csharp</td><td>C#</td></tr>
                                                        <tr><td>cpp</td><td>C/C++</td></tr>
                                                        <tr><td>css</td><td>CSS</td></tr>
                                                        <tr><td>delphi</td><td>Delphi, Pascal</td></tr>
                                                        <tr><td>diff</td><td>Diff/Patch</td></tr>
                                                        <tr><td>erl</td><td>Erlang</td></tr>
                                                        <tr><td>groovy</td><td>Groovy</td></tr>
                                                        <tr><td>js</td><td>JavaScript</td></tr>
                                                        <tr><td>java</td><td>Java</td></tr>
                                                        <tr><td>jfx</td><td>JavaFX</td></tr>
                                                        <tr><td>pl</td><td>Perl</td></tr>
                                                        <tr><td>php</td><td>PHP</td></tr>
                                                        <tr><td>plain</td><td>Plain Text</td></tr>
                                                        <tr><td>ps</td><td>PowerShell</td></tr>
                                                        <tr><td>py</td><td>Python</td></tr>
                                                        <tr><td>ruby</td><td>Ruby</td></tr>
                                                        <tr><td>scala</td><td>Scala</td></tr>
                                                        <tr><td>sql</td><td>SQL</td></tr>
                                                        <tr><td>vb</td><td>Visual Basic</td></tr>
                                                        <tr><td>xml</td><td>XML,HTML,XML,XSLT</td></tr>
                                                    </tbody>
                                                </table></td></tr>
            </table>
            <h3>Success Response</h3>
            <p><a href="#top">Standard response object (JSON)</a>. Data field contains a single object with these
            fields.</p>
            <table class="table table-condensed">
                <tr><td>uuid</td><td>unique identifier that is the key to accessing the data</td></tr>
                <tr><td>host</td><td>preferred [scheme][hostname][:port] for future requests</td></tr>
                <tr><td>browser_uri</td><td>uri intended for humans (concat to host)</td></tr>
                <tr><td>api_uri</td><td>uri intended for api users (concat to host)</td></tr>
            </table>

            <h3>Example</h3>
            <pre class="bg">
<span class="req">$ ~ curl --data "this would be stored" \\

    http://localhost:6543/api/v1/secret?set_unlimited_views=on&maximum_hours=2</span><span class="resp">
{
    "status": 200,
    "msg": "OK",
    "data": {
        "uuid": "lcDf0mTp0YbNQPeZFzDIOdWrkz2Cat8D",
        "host": "http://localhost:6543",
        "browser_uri": "/retrieve/lcDf0mTp0YbNQPeZFzDIOdWrkz2Cat8D",
        "api_uri": "/api/v1/secret/lcDf0mTp0YbNQPeZFzDIOdWrkz2Cat8D",
    }
}
</span></pre>

            <h3>Failure Example</h3>
            <p><a href="#top">Standard response object (JSON)</a>. HTTP status will not be 200.</p>
            <pre class="bg">
<span class="req">$ ~ curl --data "this would be stored" \\

    http://localhost:6543/api/v1/secret?maximum_clicks=200</span><span class="resp">
{
    "status": -2,
    "msg": "Missing fields.",
    "data": ["MISSING", ["maximum_clicks"]]
}
</span></pre>

        </div>
        <div class="clearfix"></div>
    </div>

    <div class="row hl">
        <div class="col-sm-2">
            <h3>Secret(s)</h3>
        </div>
        <div class="col-sm-10">
            <h3>Read</h3>
            <p>The uuid is required to retrieve the stored data.</p>
            <pre class="bg req">GET /api/v1/secret/{uuid}</pre>
            <h3>Optional Arguments</h3>
            <table class="table table-condensed">
                <tr><td>?data</td><td>expects boolean; default: false;</td></tr>
                <tr><td>?meta</td><td>expects boolean; default: false;<br/>
                                      returns only the meta-data (doesn't not count as a view if it exists)<br/></td></tr>
            </table>
            <h3>Success Response</h3>
            <p><a href="#top">Standard response object (JSON)</a>. Data field contains a single object with these
            fields.</p>
            <table class="table table-condensed">
                <tr><td>snippet_type</td><td>string</td></tr>
                <tr><td>expiry_time</td><td>string</td></tr>
                <tr><td>remaining_reads</td><td>integer</td></tr>
                <tr><td>can_early_expire</td><td>boolean</td></tr>
                <tr><td>can_unlimited_views</td><td>boolean</td></tr>
                <tr><td>stored_data</td><td>string</td></tr>
            </table>
            
            <h3>Example</h3>
            <p>Just a standard API grab.</p>
            <pre class="bg">
<span class="req">$ ~ curl http://localhost:6543/api/v1/secret/lcDf0mTp0YbNQPeZFzDIOdWrkz2Cat8D</span><span class="resp">
{
    "status": 0,
    "msg": "OK",
    "data": {
        "snippet_type": "",
        "expiry_time": "2015-09-27 20:42:06.533176",
        "remaining_reads": "4",
        "can_early_expire": true,
        "can_unlimited_views": false,
        "stored_data": "this would be stored",
    }
}
</span></pre>
            <p>Some data-only, better for some kinds of script use.</p>
            <pre class="bg">
<span class="req">$ ~ curl http://localhost:6543/api/v1/secret/lcDf0mTp0YbNQPeZFzDIOdWrkz2Cat8D?data</span><span class="resp">
this would be stored
</span></pre>

            <h3>Failure Example</h3>
            <p>Lookup of an expired/deleted secret, HTTP status will be 404.</p>
            <pre class="bg">
<span class="req">$ ~ curl http://localhost:6543/api/v1/secret/lcDf0mTp0YbNQPeZFzDIOdWrkz2Cat8D</span><span class="resp">
{
    "status": 0,
    "msg": "OK",
    "data": null
}
</span></pre>

            <p>Throttled. Please don't hammer me.</p>
            <pre class="bg">
<span class="req">$ ~ curl http://localhost:6543/api/v1/secret/lcDf0mTp0YbNQPeZFzDIOdWrkz2Cat8D</span><span class="resp">
{
    "status": -4,
    "msg": "Request has been throttled.",
    "data": ["THROTTLE", [20]]
}
</span></pre>
        </div>
        <div class="clearfix"></div>
    </div>

    <div class="row hl">
        <div class="col-sm-2">
            <h3>Secret(s)</h3>
        </div>
        <div class="col-sm-10">
            <h3>Deleting Early</h3>
            <p>The uuid is required to delete early.</p>
            <pre class="bg req">DELETE /api/v1/secret/{uuid}</pre>
            <h3>Success & Failure Response(s)</h3>
            <p><a href="#top">Standard response object (JSON)</a>, status will be 0, msg "OK". Data
            will mirror the HTTP Response Code.</p>
            <table class="table table-condensed">
                <tr><th>Response Code</th><th>Reason</th></tr>
                <tr><th>200</th><th>Data was found and deleted successfully.</th></tr>
                <tr><th>404</th><th>Data was not found or has already expired.</th></tr>
                <tr><th>405</th><th>Data was found, but could not be deleted due to early_expire flag.</th></tr>
            </table>
            HTTP response will
            be 200 if data was deleted. HTTP 404 if not found (or already expired), HTTP 405 if found
            and not allowed for early expire.</p>
        </div>
    </div>

</div>

</%block>
