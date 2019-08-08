#include <hpx/hpx_init.hpp>
#include <Db.hpp>

using database::Db;

int hpx_main(int argc,char **argv)
{
  auto loc = hpx::find_here();

  Db db(hpx::components::new_<database::server::Db>(loc));

  db.add("hello").wait();
  db.add("world").wait();

  std::vector<std::string> vec{"apple","orange","pear"};
  db.add_vec(vec).wait();

  std::cout << db.contains("hello").get() << std::endl;
  std::cout << db.contains("goodbye").get() << std::endl;
  std::cout << db.contains("pear").get() << std::endl;

  return hpx::finalize();
}

int main(int argc,char **argv)
{
  return hpx::init(argc, argv);
}
