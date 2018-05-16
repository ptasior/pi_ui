% rebase('base.tpl')

<div>
    <h1>Setup</h1>
    <form action="/setupSave" method="post">
        artist: <input name="artist" type="text" 
                % try:
                    value="{{data['lastFm']['artist']}}"
                % except:
                    % pass
                % end
            />
        <input value="Save" type="submit" />
    </form>
</div>

