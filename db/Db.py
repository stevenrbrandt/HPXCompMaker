from comp import *

# Note that svec and Bool exist in comp, but we
# add these types here to show how the create type
# mechanism works.
create_type("myvec",alt="std::vector",is_template=True)
create_type("bool")

@Component(namespace='database',headers=['algorithm'])
class Db:

    table : myvec[str] = default

    # This method is not exposed on the client
    @server_only
    def sort_me(self) -> None:
        cplusplus('std::sort(table.begin(), table.end());')

    def add(self, entry : str) -> None:
        cplusplus("""
        table.push_back(entry);
        sort_me();
        """)

    def add_vec(self, entries : myvec[str]) -> None:
        """ Add a bunch of things at once """
        cplusplus("""
        for(auto i=entries.begin();i != entries.end();++i)
            table.push_back(*i);
        sort_me();
        """)

    def contains(self, entry : str) -> bool:
        cplusplus("""
        return  std::binary_search(table.begin(), table.end(), entry);
        """)
