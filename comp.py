#!/usr/bin/python3
import inspect
import ast
from typing import List, Dict, NewType
import numpy as np
import re
from functools import partial

class FuncDesc:
    """
    Describe a function: it's name, arguments
    and return type.
    """
    def __init__(self,name,args,rettype,body=None):
        self.name = name
        self.rettype = rettype
        self.args = args
        self.body = body
    def __str__(self):
        s = ""
        s += self.name
        s += "("
        sep = ""
        for arg, type in self.args:
            s += sep + arg+": "+type
            sep = ", "
        s += ") -> "+self.rettype
        return s

class ComponentDesc:
    """
    Describe a component, including
    the namespace it lives in, the headers
    it needs, and the fields and functions
    it requires.
    """
    def __init__(self,cname):
        self.headers = []
        self.cname = cname
        self.namespace = None
        self.funcs = {}
        self.fields = {}
    def addfield(self,typef,namef,valf):
        self.fields[namef] = (typef, valf)
    def addfunc(self,func):
        self.funcs[func.name] = func
    def setret(self,rettype):
        self.rettype = rettype
    def setnamespace(self,namespace):
        self.namespace = namespace
    def createboilerplate(self):
        pass

    def server_name(self):
        if self.namespace is None:
            return "server::"+self.cname
        else:
            return self.namespace+"::server::"+self.cname

    def full_name(self):
        if self.namespace is None:
            return self.cname
        else:
            return self.namespace+"::"+self.cname

    def __str__(self):
        s = ""
        s += "component: "+self.cname+"\n"
        for f in self.fields.keys():
            t, v = self.fields[f]
            s += "   %s %s = %s;\n" % (t,f,v)
        s += '\n'
        for f in self.funcs.keys():
            s += "   " + str(self.funcs[f]) + "\n"
        return s

def getval(ty):
    """
    Return a value, e.g. a specific number or string
    from an AST element.
    """
    t = type(ty)
    if ty is None:
        return None
    elif t == int:
        return str(ty)
    elif t == ast.NameConstant:
        return ty.value
    elif t == ast.Name:
        return ty.id
    elif t == ast.Num:
        return str(ty.n)
    elif t == ast.USub:
        return "-"
    elif t == ast.UnaryOp:
        return getval(ty.op)+getval(ty.operand)
    elif t == ast.Str:
        s = re.sub(r'"',r'\"',ty.s)
        s = re.sub('\n',r'\\n',s)
        return '"'+s+'"'
    else:
        print(t,ty,dir(ty))
        raise Exception(ty)

def gettype(ty):
    """
    Extract a C++ type from an AST element.
    """
    global type_names
    if ty is None:
        return "None"
    t = type(ty)
    if t == ast.Name:
        if ty.id in type_names.keys():
            return type_names[ty.id]
        return ty.id
    elif t in [np.float64]:
        return str(t)
    elif t in [ast.Index, ast.NameConstant]:
        return gettype(ty.value)
    elif t in [ast.Attribute]:
        return gettype(ty.value)+"."+gettype(ty.attr)
    elif t == ast.Subscript:
        return gettype(ty.value)+'['+gettype(ty.slice)+']'
    elif t == ast.Tuple:
        # If we're processing a Dict[str,str]
        # the "str,str" part is an ast.Tuple
        s = ''
        sep = ''
        for e in ty.elts:
            s += sep + gettype(e)
            sep = ','
        return s
    elif t == ast.Call:
        if ty.func.id == "Ref":
            return "%s&" % gettype(ty.args[0])
        elif ty.func.id == "Const":
            return "%s const" % gettype(ty.args[0])
        elif ty.func.id == "Move":
            return "%s&&" % gettype(ty.args[0])
        elif ty.func.id == "Ptr":
            return "%s*" % gettype(ty.args[0])
        else:
            s = ty.func.id + "<"
            for i in len(ty.args):
                if i > 0:
                    s += ","
                arg = ty.args[i]
                s += gettype(arg) 
            s += ">"
            return s
    elif type(ty) == str:
        print(ty)
        raise Exception("?")
    else:
        print(ty.func.id)
        print(ty.args,"//",dir(ty.args[0]))
        print(ty.args[0].s, ty.args[1].id)
        print("<<",ty.__class__.__name__,">>",dir(ty))
        raise Exception("?")

def visittree(tree,cdesc):
    """
    Visits the AST tree for the component definition
    and identifies all the fields and functions with
    their types.
    """
    nm = tree.__class__.__name__
    if nm in ["Module"]:
        # tree.body is a list
        for k in tree.body:
            cdesc = visittree(k,cdesc)

    elif nm in ["ClassDef"]:
        assert cdesc is None

        # Create the ComponentDesc object
        cdesc = ComponentDesc(tree.name)
        for k in tree.body:
            cdesc = visittree(k,cdesc)

    elif nm in ["FunctionDef"]:
        args = []
        code = None
        for f in tree.body:
            if type(f) == ast.Expr and type(f.value) == ast.Call:
                code = f.value.args[0].s
        for a in tree.args.args:
            if a.arg != "self":
                args += [(a.arg, gettype(a.annotation))]
        rtype = gettype(tree.returns)
        cdesc.addfunc(FuncDesc(tree.name, args, rtype, code))

    # Process annotated assignments
    elif nm == "AnnAssign":
        cdesc.addfield(
            gettype(tree.annotation),
            getval(tree.target),
            getval(tree.value))

    return cdesc

def ttran_(n):
    "A helper for ttran in translating Python names to C++ names"
    if n == "np.float32":
        return "std::float32_t";
    elif n == "np.float64":
        return "std::float64_t";
    elif n == "np.int64":
        return "std::int64_t";
    elif n == "str":
        return "std::string"
    elif n == "None":
        return "void";
    elif n == "List":
        return "std::vector"
    elif n == "Dict":
        return "std::map"
    elif n == '[':
        return '<'
    elif n == ']':
        return '>'
    else:
        return n

def ttran(n):
    "Translate Python names to C++ names"
    s = ''
    for i in re.finditer(r'[\w\.]+|.',n):
        s += ttran_(i.group(0))
    return s

def mkdef(n):
    """
    Turns non-word characters into underscore
    and makes everything upper case.
    """
    return re.sub(r'\W','_',n.upper())

def Component_(a,kwargs):
    global server_only_funcs
    src = inspect.getsource(a)
    tree = ast.parse(src)

    # Construct a ComponentDesc object
    c = visittree(tree,None)

    if "namespace" in kwargs:
        c.namespace = kwargs["namespace"]
    if "headers" in kwargs:
        c.headers = kwargs["headers"]
    print("c:",c)

    # Create the main header file name
    fname = c.cname + ".hpp"

    # fconst is used to make the
    # #ifndef ....
    # #define ....
    # macros at the top of the headers.
    if c.namespace is not None:
        fconst = mkdef(c.namespace+"::"+fname)
    else:
        fconst = mkdef(fname)

    with open(fname,"w") as fd:
        print("#ifndef %s" % fconst,file=fd)
        print("#define %s 1" % fconst,file=fd)

        # Insert headers...
        print("""
#include <hpx/hpx.hpp>
#include <hpx/include/actions.hpp>
#include <hpx/include/lcos.hpp>
#include <hpx/include/components.hpp>
#include <hpx/include/serialization.hpp>
""",file=fd)
        for h in c.headers:
            print("#include <%s>" % h,file=fd)

        # Insert namespace declarations...
        if c.namespace is not None:
            for nm in c.namespace.split("::"):
                print("namespace %s {" % nm,file=fd)
        print("namespace server {",file=fd)

        # Insert start of class
        print("""
struct HPX_COMPONENT_EXPORT {cname}
    : hpx::components::component_base<{cname}>
{{
    /**
     * All internal state.
     */
""".format(cname=c.cname),file=fd)

        # Insert declared fields
        for k in sorted(c.fields.keys()):
            t,v = c.fields[k]
            t = ttran(t)
            if v == "default":
                print("    %s %s;" % (t,k),file=fd)
            elif v is None:
                print("    %s %s = nullptr;" % (t,k),file=fd)
            else:
                print("    %s %s = %s;" % (t,k,v),file=fd)

        # Insert functions
        print("    /* Functions */",file=fd)

        print(file=fd)
        if "__init__" not in c.funcs.keys():
            # Add empty constructor and destructor if need be
            print("    {clazz}() {{}}".format(clazz=c.cname),file=fd)
        if "__del__" not in c.funcs.keys():
            print("    ~{clazz}() {{}}".format(clazz=c.cname),file=fd)

        for k in sorted(c.funcs.keys()):
            func = c.funcs[k]
            print(file=fd)

            # Special case for __init__...
            if func.name == "__del__":
                if func.body is None:
                    print("    ~%s();" % c.cname,file=fd)
                else:
                    print("    ~%s() { %s }" % (c.cname,func.body),file=fd)
                continue
            elif func.name == "__init__":
                print("    %s(" % c.cname,end='',file=fd)

            # All non-special functions...
            else:
                print("    %s %s(" % (ttran(func.rettype), func.name),end='',file=fd)

            # Print function arguments...
            sep = ""
            for argname, argtype in func.args:
                print("%s%s %s" % (sep, ttran(argtype), argname),end='',file=fd)
                sep = ", "

            # End function def.
            if func.body is None:
                print(");",file=fd)
            else:
                print(") {",func.body,"}",file=fd)

            # If this isn't a server_only function, create a component action
            if func.name != "__init__":
                if func.name not in server_only_funcs:
                    print("    HPX_DEFINE_COMPONENT_ACTION(%s, %s);" %
                        (c.server_name(), func.name),file=fd)

        print("}; // end server code",file=fd)
        print(file=fd)
        print("} // end server namespace",file=fd)

        # End user supplied namespaces
        if c.namespace is not None:
            print(file=fd)
            for nm in c.namespace.split("::"):
                print("} // namespace %s" % nm,file=fd)

        # Register action declarations...
        print(file=fd)
        for k in sorted(c.funcs.keys()):
            if k == "__init__":
                continue
            if k == "__del__":
                continue
            if k in server_only_funcs:
                continue
            print("HPX_REGISTER_ACTION_DECLARATION(",file=fd)
            print("  %s::%s_action, %s);" %
                (c.server_name(),k,c.server_name()),file=fd)

        # Re-open user namespace for client code...
        print(file=fd)
        if c.namespace is not None:
            for nm in c.namespace.split("::"):
                print("namespace %s {" % nm,file=fd)

        client  = """
struct {clazz} : hpx::components::client_base<{client_class},{server_class}>
{{
    typedef hpx::components::client_base<{client_class},{server_class}> base_type;

    {clazz}(hpx::future<hpx::naming::id_type> && f)
        : base_type(std::move(f))
    {{}}

    {clazz}(hpx::naming::id_type && f)
        : base_type(std::move(f))
    {{}}

    ~{clazz}(){{}}""".format(
        clazz=c.cname,
        client_class=c.full_name(),
        server_class=c.server_name())
        print(client,file=fd)

        # Re-traverse functions so that we can
        # define them in the client
        for k in sorted(c.funcs.keys()):
            func = c.funcs[k]
            if k in server_only_funcs:
                continue
            print(file=fd)

            # skip init
            if func.name == "__init__":
                continue
            if func.name == "__del__":
                continue

            # Beginning of function through the function name...
            elif ttran(func.rettype).startswith("hpx::future<"):
                print("    %s %s(" % (ttran(func.rettype), func.name),end='',file=fd)
            else:
                print("    hpx::future<%s> %s(" % (ttran(func.rettype), func.name),end='',file=fd)

            # Arg types for the function...
            sep = ""
            for argname, argtype in func.args:
                print("%s%s %s" % (sep, ttran(argtype), argname),end='',file=fd)
                sep = ", "

            # End function prototype, begin function body...
            print(") {",file=fd)

            # Function body, just a call to async with the action...
            print("        return hpx::async<%s::%s_action>(this->get_id()" %
                (c.server_name(),k),end='',file=fd)

            # Each arg in the call...
            for argname, argtype in func.args:
                print(",%s" % (argname),end='',file=fd)

            # End of the call.
            print(");",file=fd)

            # End of function body.
            print("    }",file=fd)

            ###
            # Begin static version of the function call...
            print("    static hpx::future<%s> %s(hpx::naming::id_type& this_id" % (ttran(func.rettype), func.name),end='',file=fd)

            # Arg types for the static version...
            for argname, argtype in func.args:
                print(",%s %s" % (ttran(argtype), argname),end='',file=fd)

            # End of prototype, begin function body for static...
            print(") {",file=fd)

            #  call to async...
            print("        return hpx::async<%s::%s_action>(this_id" %
                (c.server_name(),k),end='',file=fd)

            # args for async call...
            for argname, argtype in func.args:
                print(",%s" % (argname),end='',file=fd)

            # end of call...
            print(");",file=fd)

            # end of static function.
            print("    }",file=fd)

        print("}; // end client code",file=fd)

        # Close user namespace
        if c.namespace is not None:
            print(file=fd)
            for nm in c.namespace.split("::"):
                print("} // namespace %s" % nm,file=fd)

        print(file=fd)
        print("#endif",file=fd)

    # Macros for register the component and its actions
    fmname = c.cname + "_macros.cpp"
    with open(fmname,"w") as fd:
        print("""#include <{inc}>
HPX_REGISTER_COMPONENT_MODULE();

typedef hpx::components::component<
    {server_class}
> {clazz}_type;

HPX_REGISTER_COMPONENT({clazz}_type, {clazz});
        """.format(clazz=c.cname,server_class=c.server_name(),inc=fname),file=fd)

        for k in sorted(c.funcs.keys()):
            if k == "__init__":
                continue
            if k == "__del__":
                continue
            if k in server_only_funcs:
                continue
            print("""HPX_REGISTER_ACTION(
    {server_class}::{func}_action, {clazz}_{func}_action);
            """.format(clazz=c.cname,server_class=c.server_name(),func=k),file=fd)
    return a

def Component(**kwargs):
    global server_only_funcs, locked_funcs
    server_only_funcs = []
    locked_funcs = []
    return lambda a : Component_(a,kwargs)

class basic_type:
    def __init__(self,name=None):
        if name is not None:
            self.full_name = name

class template_type:
    def __init__(self,name=None):
        if name is not None:
            self.full_name = name
    def __getitem__(self,a):
        pass
    def __getslice__(self,*a):
        pass

type_names = {}

def create_type(name,alt=None,is_template=False):
    global type_names
    assert name is not None
    if alt is not None:
        type_names[name] = alt
    else:
        type_names[name] = name
    stack = inspect.stack()
    if 1 < len(stack):
        index = 1
    else:
        index = 0
    if is_template:
        stack[index].frame.f_globals[name] = template_type(name)
    else:
        stack[index].frame.f_globals[name] = basic_type(name)

def locked_(m,a):
    global locked_funcs
    locked_funcs += [(a.__name__,m)]
    return a

def locked(m):
    """
    This describes a function that is wrapped in a lock.
    """
    return partial(locked_,m)

def server_only(a):
    """
    The server_only function annotation identifies a method that
    will not be exported by the component.
    """
    global server_only_funcs
    server_only_funcs += [a.__name__]
    return a

def Const(_):
    "Used to identify const types"
    pass

def Ref(_):
    "Used to identify references"
    pass
def Ptr(_):
    "Used to identify pointer types"
    pass


#id_type = basic_type("hpx::naming::id_type")
#smap = template_type("std::map")
create_type("id_type",alt="hpx::naming::id_type")
create_type("smap",alt="std::map",is_template=True)

default = object()

#########
# Component definitions
