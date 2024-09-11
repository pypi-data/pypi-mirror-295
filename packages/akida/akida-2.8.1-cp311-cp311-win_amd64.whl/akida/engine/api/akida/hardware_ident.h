#pragma once

#include <cstdint>
#include <vector>

namespace akida::hw {

struct Ident {
  uint8_t col;
  uint8_t row;
  uint8_t id;

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator==(const Ident& other) const {
    return col == other.col && row == other.row && id == other.id;
  }

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator!=(const Ident& other) const { return !(*this == other); }

  // TODO: can be replaced by default Three-way comparison in C++20
  bool operator<(const Ident& other) const {
    return (col < other.col) || ((col == other.col) && (row < other.row)) ||
           ((col == other.col) && (row == other.row) && (id < other.id));
  }
};

using IdentVector = std::vector<Ident>;

constexpr Ident HRC_IDENT = Ident{0, 0, 0};

}  // namespace akida::hw