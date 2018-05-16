% rebase('base.tpl')

% def mprint(menu, path=''):
    <ul>
    % for i in menu:
        % if menu[i] == 'script':
            <li><a href="execute/{{(path+'.'+i)[1:]}}">{{i}}</a></li>
        % elif len(menu[i]):
            <li>{{i}}</li>
            % mprint(menu[i], path+'.'+i)
        % end
    % end
    </ul>
% end

<div>
    <h1>Menu</h1>
    % if not len(items):
        Menu is empty
    %else:
        % mprint(items)
    %end
</div>

