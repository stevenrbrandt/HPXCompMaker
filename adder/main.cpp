#include <hpx/hpx_init.hpp>
#include <Adder.hpp>

using adder::Adder;

int hpx_main(int argc,char **argv)
{
  auto loc = hpx::find_here();

  Adder ad(hpx::components::new_<adder::server::Adder>(loc));
  std::cout << ad.get().get() << std::endl;
  ad.add(3).wait();
  std::cout << ad.get().get() << std::endl;
  ad.add_value("fish",4).wait();
  std::cout << ad.get_value("fish").get() << std::endl;
  return hpx::finalize();
}

int main(int argc,char **argv)
{
  return hpx::init(argc, argv);
}
