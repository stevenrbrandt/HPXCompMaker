#include <PrintUtil.hpp>
HPX_REGISTER_COMPONENT_MODULE();

typedef hpx::components::component<
    printutil::server::PrintUtil
> PrintUtil_type;

HPX_REGISTER_COMPONENT(PrintUtil_type, PrintUtil);
        
HPX_REGISTER_ACTION(
    printutil::server::PrintUtil::__del___action, PrintUtil___del___action);
            
HPX_REGISTER_ACTION(
    printutil::server::PrintUtil::hello_action, PrintUtil_hello_action);
            
HPX_REGISTER_ACTION(
    printutil::server::PrintUtil::hello2_action, PrintUtil_hello2_action);
            
HPX_REGISTER_ACTION(
    printutil::server::PrintUtil::write_action, PrintUtil_write_action);
            
