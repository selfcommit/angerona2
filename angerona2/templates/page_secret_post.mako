<%inherit file="angerona2:templates/base.mako" />
<%block name="AddedJS">

<script type="text/javascript">

//adapted from: http://stackoverflow.com/a/30905277/274549
copyToClipboard = function (d) {
    var $temp = $("<input />");
    $("body").append($temp);
    $temp.val(d).select();

    var result = false;
    try {
        result = document.execCommand("copy");
    } catch (err) {
        console.log("Copy error: " + err);
    }

    $temp.remove();
    return result;
}

$(document).ready(function() {
    $('button.clipboard').click(function() {
        var link = $(this).parent().siblings('input[type=text]:first').val();
        if(!copyToClipboard(link)) {
            $(this).parents('div.row:first')
                .append('<p>Copy/paste failed, please copy the link instead.</p>')
                .find('input[type=text]:first')
                    .replaceWith(
                        $('<a/>')
                            .attr('href', link)
                            .text(link)
                    )
                .end();
            $(this).parent().remove();
        }
    });

    $('input[type=text]').click(function() {
        $(this).select();
    });
});

</script>

</%block>
<%block name="AddedCSS">

<style type="text/css">
    div.row div>div.row {
        margin-bottom: 2em;
    }
</style>

</%block>
<%block name="BlockContent">

<div class="row">
    <div class="col-md-12">
        <h3 class="text-center">Sharable Links</h3>
        <p>Below, you may find the various links for sharing this data out.</p>

        <p>Links are good for: ${friendly_time} or ${friendly_clicks} clicks (whichever comes first).</p>
        <p>Links ${friendly_delete}.</p>

        <div class="row">
            <label class="control-label">Require click to show data (for browsers)</label>
            <div class="input-group">
                <input type="text" class="form-control" readonly
                       value="${request.route_url('retrieve', uuid=uuid)}" />
                <span class="input-group-btn">
                    <button type="button" class="btn btn-default clipboard" aria-label="Copy to Clipboard">
                        Copy <span class="glyphicon glyphicon-copy" aria-hidden="true"></span>
                    </button>
                </span>
            </div>
        </div>
        <div class="row">
            <label class="control-label">Immediately show data (for browser)</label>
            <div class="input-group">
                <input type="text" class="form-control" readonly
                       value="${request.route_url('retrieve', uuid=uuid)}?show" />
                <span class="input-group-btn">
                    <button type="button" class="btn btn-default clipboard" aria-label="Copy to Clipboard">
                        Copy <span class="glyphicon glyphicon-copy" aria-hidden="true"></span>
                    </button>
                </span>
            </div>
        </div>
        <div class="row">
            <label class="control-label">JSON (for scripts)</label>
            <div class="input-group">
                <input type="text" class="form-control" readonly
                       value="${request.route_url('api_secret:uuid', uuid=uuid)}" />
                <span class="input-group-btn">
                    <button type="button" class="btn btn-default clipboard" aria-label="Copy to Clipboard">
                        Copy <span class="glyphicon glyphicon-copy" aria-hidden="true"></span>
                    </button>
                </span>
            </div>
        </div>
        <div class="row">
            <label class="control-label">Just the data (for scripts)</label>
            <div class="input-group">
                <input type="text" class="form-control" readonly
                       value="${request.route_url('api_secret:uuid', uuid=uuid)}?data" />
                <span class="input-group-btn">
                    <button type="button" class="btn btn-default clipboard" aria-label="Copy to Clipboard">
                        Copy <span class="glyphicon glyphicon-copy" aria-hidden="true"></span>
                    </button>
                </span>
            </div>
        </div>
    </div>
</div>

</%block>