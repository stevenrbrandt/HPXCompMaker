#ifndef PRINTUTIL__PRINTUTIL_HPP
#define PRINTUTIL__PRINTUTIL_HPP 1

#include <hpx/hpx.hpp>
#include <hpx/include/actions.hpp>
#include <hpx/include/lcos.hpp>
#include <hpx/include/components.hpp>
#include <hpx/include/serialization.hpp>

namespace printutil {
namespace server {

struct HPX_COMPONENT_EXPORT PrintUtil
    : hpx::components::component_base<PrintUtil>
{
    /**
     * All internal state.
     */

    /* Functions */


    ~PrintUtil();

    PrintUtil() { /*comment*/ }

    void hello() { std::cout << "Hello" << std::endl; }
    HPX_DEFINE_COMPONENT_ACTION(printutil::server::PrintUtil, hello);

    void hello2();
    HPX_DEFINE_COMPONENT_ACTION(printutil::server::PrintUtil, hello2);

    void write(std::string s) { std::cout << s << std::endl; }
    HPX_DEFINE_COMPONENT_ACTION(printutil::server::PrintUtil, write);
}; // end server code

} // end server namespace

} // namespace printutil

HPX_REGISTER_ACTION_DECLARATION(
  printutil::server::PrintUtil::__del___action, printutil::server::PrintUtil);
HPX_REGISTER_ACTION_DECLARATION(
  printutil::server::PrintUtil::hello_action, printutil::server::PrintUtil);
HPX_REGISTER_ACTION_DECLARATION(
  printutil::server::PrintUtil::hello2_action, printutil::server::PrintUtil);
HPX_REGISTER_ACTION_DECLARATION(
  printutil::server::PrintUtil::write_action, printutil::server::PrintUtil);

namespace printutil {

struct PrintUtil : hpx::components::client_base<printutil::PrintUtil,printutil::server::PrintUtil>
{
    typedef hpx::components::client_base<printutil::PrintUtil,printutil::server::PrintUtil> base_type;

    PrintUtil(hpx::future<hpx::naming::id_type> && f)
        : base_type(std::move(f))
    {}

    PrintUtil(hpx::naming::id_type && f)
        : base_type(std::move(f))
    {}

    ~PrintUtil(){}

    hpx::future<void> __del__() {
        return hpx::async<printutil::server::PrintUtil::__del___action>(this->get_id());
    }
    static hpx::future<void> __del__(hpx::naming::id_type& this_id) {
        return hpx::async<printutil::server::PrintUtil::__del___action>(this_id);
    }


    hpx::future<void> hello() {
        return hpx::async<printutil::server::PrintUtil::hello_action>(this->get_id());
    }
    static hpx::future<void> hello(hpx::naming::id_type& this_id) {
        return hpx::async<printutil::server::PrintUtil::hello_action>(this_id);
    }

    hpx::future<void> hello2() {
        return hpx::async<printutil::server::PrintUtil::hello2_action>(this->get_id());
    }
    static hpx::future<void> hello2(hpx::naming::id_type& this_id) {
        return hpx::async<printutil::server::PrintUtil::hello2_action>(this_id);
    }

    hpx::future<void> write(std::string s) {
        return hpx::async<printutil::server::PrintUtil::write_action>(this->get_id(),s);
    }
    static hpx::future<void> write(hpx::naming::id_type& this_id,std::string s) {
        return hpx::async<printutil::server::PrintUtil::write_action>(this_id,s);
    }
}; // end client code

} // namespace printutil

#endif
