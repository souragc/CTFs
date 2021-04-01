#ifndef STMT_H
#define STMT_H
#include <fstream>
#include <iostream>
#include <string>
#include <tao/pegtl.hpp>
#include <tao/pegtl/analyze.hpp>
#include <tao/pegtl/contrib/parse_tree.hpp>

#include "ast.h"
using namespace tao::pegtl;
namespace pegtl = tao::TAOCPP_PEGTL_NAMESPACE;

namespace ast {
struct stmt : node {
  virtual void emit(ostream& os){};
};
struct stmt_block : stmt {
  void emit(ostream& os) override;
};

struct expr_stmt : stmt {
  void emit(ostream& os) override;
};
struct if_stmt : stmt {
  void emit(ostream& os) override;
};
struct while_stmt : stmt {
  void emit(ostream& os) override;
};
struct return_stmt : stmt {
  void emit(ostream& os) override;
};
struct assign_stmt : stmt {
  void emit(ostream& os) override;
};
struct typed_def_stmt : stmt {
  void emit(ostream& os) override;
};
struct var_decl : stmt {
  void emit(ostream& os) override;
};
struct typed_arg_decl_list : stmt {
  void emit(ostream& os) override;
};
}  // namespace ast

namespace parser {
template <>
struct action<stmt_block> : action_impl<ast::stmt_block> {};
template <>
struct action<if_stmt> : action_impl<ast::if_stmt> {};
template <>
struct action<while_stmt> : action_impl<ast::while_stmt> {};
template <>
struct action<return_stmt> : action_impl<ast::return_stmt> {};
template <>
struct action<expr_stmt> : action_impl<ast::expr_stmt> {};
template <>
struct action<stmt> : action_impl<ast::stmt> {};
template <>
struct action<assign_stmt> : action_impl<ast::assign_stmt> {};
template <>
struct action<typed_def_stmt> : action_impl<ast::typed_def_stmt> {};
template <>
struct action<var_decl> : action_impl<ast::var_decl> {};
template <>
struct action<typed_arg_decl_list> : action_impl<ast::typed_arg_decl_list> {};
}  // namespace parser

#endif
