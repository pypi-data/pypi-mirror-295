/*
 *  Copyright (c) 2023 hikyuu.org
 *
 *  Created on: 2023-12-25
 *      Author: fasiondog
 */

#pragma once

#include "hikyuu/trade_sys/system/System.h"
#include "hikyuu/trade_manage/Performance.h"
#include "hikyuu/utilities/thread/thread.h"

namespace hku {

struct HKU_API AnalysisSystemWithBlockOut {
    string market_code;  ///< 证券代码
    string name;         ///< 证券名称
    PriceList values;    ///< 统计各项指标值

    AnalysisSystemWithBlockOut() = default;
    AnalysisSystemWithBlockOut(const AnalysisSystemWithBlockOut& other) = default;
    AnalysisSystemWithBlockOut(AnalysisSystemWithBlockOut&& rv)
    : market_code(std::move(rv.market_code)),
      name(std::move(rv.name)),
      values(std::move(rv.values)) {}

    AnalysisSystemWithBlockOut& operator=(const AnalysisSystemWithBlockOut&) = default;
    AnalysisSystemWithBlockOut& operator=(AnalysisSystemWithBlockOut&& rv) {
        HKU_IF_RETURN(this == &rv, *this);
        market_code = std::move(rv.market_code);
        name = std::move(rv.name);
        values = std::move(rv.values);
        return *this;
    }
};

vector<AnalysisSystemWithBlockOut> HKU_API analysisSystemList(const SystemList& sys_list,
                                                              const StockList& stk_list,
                                                              const KQuery& query);

vector<AnalysisSystemWithBlockOut> HKU_API analysisSystemList(const StockList& stk_list,
                                                              const KQuery& query,
                                                              const SystemPtr& pro_sys);

}  // namespace hku
