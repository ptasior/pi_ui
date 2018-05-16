% rebase('base.tpl')

<div>
    <h1>Playlist</h1>
    % if not len(items):
        Playlist is empty
    %else:
        % for i in items:
            {{str(i)}}<br>
        %end
    %end
</div>

