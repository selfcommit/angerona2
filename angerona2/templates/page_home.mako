<%inherit file="angerona2:templates/base.mako" />
<%block name="BlockContent">

    <div class="jumbotron">
        <div class="container">
            <h1>Angerona</h1>
            <p>/ˌæn dʒəˈroʊ nə/</p>
            <p>In mythology, Angerona was the deity which protected Rome by
            keeping the sacred name of the city from its enemies; aptly-named,
            this project is a keeper of secrets. Unlike its namesake, these
            secrets are only protected for a finite amount of time or shares,
            after which they evaporate into the nether that is the ones and
            zeros of the modern world.</p>
            
            <div class="text-center">
                <a class="btn btn-success btn-lg" href="${request.route_url('secret')}" role="button">Share a Secret</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-8">
            <h2>Usage</h2>
            <p>Angerona is designed to allow the <em>safer</em> transfer of sensitive
            information over an insecure (but not real-time) attackable channel.
            The main use-cases this type of security is useful for are also most
            obvious:</p>
    
            <ul>
                <li>Passwords over email</li>
                <li>Passwords over logged chat</li>
                <li>One-off passwords sent to other people</li>
            </ul>
            
            <p>As quick feature, a syntax highlighter piece was thrown in to quickly
            share snippets of code back and forth (especially code that contains
            secrets)</p>

            <p>Under <strong>no circumstances</strong> should all parts of a
            credential be sent over the same insecure channel of communication.
            An adversary intercepting that channel would have the entire
            credential.</p>
            
            <p>In other words, do <strong>not use the same Angerona link to share
            both a username/password</strong>. Ideally, you would share different
            parts of a credential over completely different channels of communication.</p>
        </div>
        <div class="col-md-4">
            <h2>About</h2>
            <p>Angerona.pw is hosted as a convenience, with no ads.</p>
            <p>Please do not abuse the service by attempting to send filedata: 
            there are <a href="https://www.google.com/#q=temporary+file+storage+service">
            platforms</a> designed for doing that instead.</p>
            <p>If you wish to host an instance yourself, Angerona.pw is written in Python
            and released under the MIT license.</p>
            <p><a class="btn btn-default" href="https://github.com/nextraztus/angerona2" role="button">View Source »</a></p>
        </div>
    </div>

</%block>