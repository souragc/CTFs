#ifndef EXPR_H
#define EXPR_H

#include <fstream>
#include <iostream>
#include <string>
#include <tao/pegtl.hpp>
#include <tao/pegtl/analyze.hpp>
#include <tao/pegtl/contrib/parse_tree.hpp>

#include "stmt.h"
using namespace tao::pegtl;
namespace pegtl = tao::TAOCPP_PEGTL_NAMESPACE;

namespace ast {
struct expr : stmt {};
struct left_expr : expr {
  // Override this if an expression has special behavior on the left of an
  // assignment.
  virtual void emit_left(ostream& os, expr* param) {
    emit(os);
    os << " = (";
    param->emit(os);
    os << ")";
  }
};
struct paren_expr : expr {
  virtual void emit(ostream& os) {
    assert(children.size() == 1);
    os << "(";
    cast<expr*>(children[0].get())->emit(os);
    os << ")";
  }
};
struct integer : expr {
  void emit(ostream& os) override {
    assert(children.size() == 0);
    os << "" << data() << "ULL";
  }
};
struct str_literal : expr {
  void emit(ostream& os) override {
    assert(children.size() == 0);
    os << "make_string(" << data() << ")";
  }
};
struct variable : left_expr {
  void emit(ostream& os) override {
    assert(children.size() == 1);
    cast<ident*>(children[0].get())->emit(os);
  }
};
}  // namespace ast
namespace parser {
template <>
struct action<paren_expr> : action_impl<ast::paren_expr> {};
template <>
struct action<integer> : action_impl<ast::integer> {};
template <>
struct action<str_literal::literal> : action_impl<ast::str_literal> {};
template <>
struct action<variable> : action_impl<ast::variable> {};
}  // namespace parser

#endif
