#include <hpx/hpx_init.hpp>
#include <PrintUtil.hpp>

using printutil::PrintUtil;

int hpx_main(int argc,char **argv)
{
  auto loc = hpx::find_here();

  PrintUtil put(hpx::components::new_<printutil::server::PrintUtil>(loc));
  put.hello().wait();
  put.hello2().wait();
  put.write("This is a message").wait();
  return hpx::finalize();
}

int main(int argc,char **argv)
{
  return hpx::init(argc, argv);
}
