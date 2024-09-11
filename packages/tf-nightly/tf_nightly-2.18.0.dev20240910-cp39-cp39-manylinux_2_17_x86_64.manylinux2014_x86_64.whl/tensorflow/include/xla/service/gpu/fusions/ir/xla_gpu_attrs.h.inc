/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace xla {
namespace gpu {
class IndexingMapAttr;
namespace detail {
struct IndexingMapAttrStorage;
} // namespace detail
class IndexingMapAttr : public ::mlir::Attribute::AttrBase<IndexingMapAttr, ::mlir::Attribute, detail::IndexingMapAttrStorage> {
public:
  using Base::Base;
  // Returns the indexing map constructed from IndexingMapAttr.
  xla::gpu::IndexingMap getIndexingMap();

  // Returns the number of indexing map results.
  int64_t getNumResults();
  static constexpr ::llvm::StringLiteral name = "xla_gpu.indexing_map";
  static constexpr ::llvm::StringLiteral dialectName = "xla_gpu";
  using Base::getChecked;
  static IndexingMapAttr get(::mlir::MLIRContext *context, ::mlir::AffineMap map, ::llvm::ArrayRef<::xla::gpu::DimVar> dim_vars, ::llvm::ArrayRef<::xla::gpu::RangeVar> range_vars, ::llvm::ArrayRef<::std::pair<::mlir::AffineExpr, ::xla::gpu::Interval>> constraints, bool is_simplified);
  static IndexingMapAttr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::mlir::AffineMap map, ::llvm::ArrayRef<::xla::gpu::DimVar> dim_vars, ::llvm::ArrayRef<::xla::gpu::RangeVar> range_vars, ::llvm::ArrayRef<::std::pair<::mlir::AffineExpr, ::xla::gpu::Interval>> constraints, bool is_simplified);
  static IndexingMapAttr get(::mlir::MLIRContext *context, const ::xla::gpu::IndexingMap&indexing_map);
  static IndexingMapAttr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, const ::xla::gpu::IndexingMap&indexing_map);
  static ::llvm::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::AffineMap map, ::llvm::ArrayRef<::xla::gpu::DimVar> dim_vars, ::llvm::ArrayRef<::xla::gpu::RangeVar> range_vars, ::llvm::ArrayRef<::std::pair<::mlir::AffineExpr, ::xla::gpu::Interval>> constraints, bool is_simplified);
  static ::llvm::LogicalResult verifyInvariants(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::AffineMap map, ::llvm::ArrayRef<::xla::gpu::DimVar> dim_vars, ::llvm::ArrayRef<::xla::gpu::RangeVar> range_vars, ::llvm::ArrayRef<::std::pair<::mlir::AffineExpr, ::xla::gpu::Interval>> constraints, bool is_simplified);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"indexing_map"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::AffineMap getMap() const;
  ::llvm::ArrayRef<::xla::gpu::DimVar> getDimVars() const;
  ::llvm::ArrayRef<::xla::gpu::RangeVar> getRangeVars() const;
  ::llvm::ArrayRef<::std::pair<::mlir::AffineExpr, ::xla::gpu::Interval>> getConstraints() const;
  bool getIsSimplified() const;
};
} // namespace gpu
} // namespace xla
MLIR_DECLARE_EXPLICIT_TYPE_ID(::xla::gpu::IndexingMapAttr)

#endif  // GET_ATTRDEF_CLASSES

