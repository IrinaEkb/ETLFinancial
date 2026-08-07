
   # Business rules for mapping SEC XBRL tags to financial statement metrics.
#     Defines which XBRL concepts belong to:
#   - Balance Sheet
#   - Income Statement
#   - Cash Flow Statement


FINANCIAL_RULES = {

# PROFIT LOSS STATEMENT

    "income_statement": {

        "premium_revenue": [

            "Revenues",
            "RevenuesFromExternalCustomers",
            "RevenueFromContractWithCustomerIncludingAssessedTax",
            "PremiumsEarnedNet"

        ],

        "medical_benefits_and_claims_expense": [

            "BenefitsLossesAndExpenses",
            "PolicyholderBenefitsAndClaimsIncurredHealthCare",
            "PolicyholderBenefitsAndClaimsIncurredNet",
            "ShortdurationInsuranceContractsIncurredClaimsAndAllocatedClaimAdjustmentExpenseNet",
            "LiabilityForUnpaidClaimsAndClaimsAdjustmentExpenseIncurredClaims",
            "PaymentsForLossesAndLossAdjustmentExpense"

        ],

        "general_administrative_expense": [

            "SellingGeneralAndAdministrativeExpense"

        ],

        "investment_income": [

            "InvestmentIncomeInterestAndDividend",
            "NetInvestmentIncome",
            "IncomeLossFromEquityMethodInvestments"

        ],

        "impairment_charges": [

            "AssetImpairmentCharges",
            "TangibleAssetImpairmentCharges"

        ],

        "depreciation_and_amortization": [

            "Depreciation",
            "DepreciationAndAmortization",
            "AmortizationOfIntangibleAssets",
            "FiniteLivedIntangibleAssetsAmortizationExpense"

        ],

        "interest_expense": [

            "InterestExpense",
            "InterestExpenseNonoperating"

        ],

        "tax_expense": [

            "IncomeTaxExpenseBenefit",
            "CurrentIncomeTaxExpenseBenefit",
            "CurrentFederalTaxExpenseBenefit",
            "CurrentForeignTaxExpenseBenefit",
            "CurrentStateAndLocalTaxExpenseBenefit",
            "DeferredIncomeTaxExpenseBenefit",
            "DeferredFederalTaxExpenseBenefit",
            "DeferredForeignTaxExpenseBenefit",
            "DeferredStateAndLocalTaxExpenseBenefit"

        ],

        "operating_income": [

            "OperatingIncomeLoss"

        ],

        "net_income": [

            "NetIncomeLoss",
            "ProfitLoss"

        ],

        "income_before_tax": [

            "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic",
            "IncomeLossFromContinuingOperationsBeforeIncomeTaxesForeign"

        ],

        "other_income_expense": [

            "OtherIncome",
            "OtherNonoperatingIncomeExpense",
            "GainLossOnSaleOfInvestments",
            "GainLossOnSaleOfPropertyPlantEquipment",
            "DebtAndEquitySecuritiesGainLoss",
            "GainLossOnContractTermination",
            "GainLossOnSaleOfBusiness",
            "DisposalGroupNotDiscontinuedOperationGainLossOnDisposal",
            "EquityMethodInvestmentRealizedGainLossOnDisposal"

        ],

        "insurance_income": [

            "CededPremiumsWritten"

        ],

        "tax_items": [

            "DeferredOtherTaxExpenseBenefit",
            "TaxAdjustmentsSettlementsAndUnusualProvisions"

        ],

        "lease_expense": [

            "LeaseAndRentalExpense",
            "OperatingLeaseCost",
            "VariableLeaseCost"

        ],

        "equity_compensation_expense": [

            "RestrictedStockExpense",
            "StockOptionPlanExpense",
            "ShareBasedCompensation"

        ],

        "restructuring_expense": [

            "RestructuringCharges"

        ],

        "insurance_related_expenses": [

            "DeferredPolicyAcquisitionCostAmortizationExpense",
            "SupplementalInformationForPropertyCasualtyInsuranceUnderwritersCurrentYearClaimsAndClaimsAdjustmentExpense",
            "SupplementalInformationForPropertyCasualtyInsuranceUnderwritersPriorYearClaimsAndClaimsAdjustmentExpense"

        ],

        "revenue": [

            "SalesRevenueNet",
            "SalesRevenueServicesNet",
            "RevenueFromContractWithCustomerExcludingAssessedTax"

        ],

        "tax_expense_items": [

            "EffectiveIncomeTaxRateContinuingOperations",
            "EffectiveIncomeTaxRateContinuingOperationsDomestic",
            "EffectiveIncomeTaxRateContinuingOperationsForeign"

        ],

        "other_expenses": [

            "BusinessCombinationAcquisitionRelatedCosts",
            "ValuationAllowancesAndReservesChargedToCostAndExpense",
            "DefinedContributionPlanCostRecognized"

        ],

        "debt_related_income_expense": [

            "DebtInstrumentRepurchaseAmount",
            "DebtInstrumentRepurchasedFaceAmount",
            "DebtInstrumentRedemptionPricePercentageOfPrincipalAmountRedeemed"

        ],

        "insurance_contract_expenses": [

            "ReinsuranceEffectOnClaimsAndBenefitsIncurredAmountCeded",
            "ShortdurationInsuranceContractsCumulativePaidClaimsAndAllocatedClaimAdjustmentExpenseNet"

        ],

        "investment_gains_losses": [

            "AvailableforsaleSecuritiesContinuousUnrealizedLossPosition12MonthsOrLongerAggregateLosses1",
            "AvailableforsaleSecuritiesContinuousUnrealizedLossPosition12MonthsOrLongerAggregateLosses2",
            "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionAggregateLosses1",
            "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionAggregateLosses2",
            "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionLessThan12MonthsAggregateLosses1",
            "AvailableforsaleSecuritiesContinuousUnrealizedLossPositionLessThan12MonthsAggregateLosses2",
            "AvailableForSaleSecuritiesGrossUnrealizedGain"

        ],

        "comprehensive_income": [

            "ComprehensiveIncomeNetOfTax"

        ],

        "lease_income": [

            "OperatingLeasesIncomeStatementSubleaseRevenue",
            "SubleaseIncome"

        ],

        "earnings_per_share": [

            "EarningsPerShareBasic",
            "EarningsPerShareDiluted"

        ]

    },



# BALANCE SHEET 

        "balance_sheet": {

        "cash_and_cash_equivalents": [

            "CashAndCashEquivalentsAtCarryingValue",
            "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
            "CashAndDueFromBanks",
            "CashRestrictedCashAndCashEquivalents",
            "BankOverdrafts"

        ],

        "investment_securities": [

            "AvailableForSaleSecurities",
            "AvailableForSaleDebtSecurities",
            "AvailableForSaleSecuritiesDebtSecurities",
            "EquityMethodInvestments",
            "EquitySecuritiesFvNi",
            "InvestmentsInDebtAndEquitySecurities"

        ],

        "premium_receivables": [

            "PremiumsReceivableAtCarryingValue",
            "ReceivablesNetCurrent",
            "OtherReceivables"

        ],

        "accounts_receivable": [

            "AllowanceForDoubtfulAccountsReceivableCurrent",
            "AccountsReceivableNetCurrent",
            "ProvisionForDoubtfulAccounts"

        ],

        "deferred_policy_acquisition_costs": [

            "DeferredPolicyAcquisitionCosts"

        ],

        "total_assets": [

            "Assets"

        ],

        "current_assets": [

            "AssetsCurrent"

        ],

        "goodwill": [

            "Goodwill"

        ],

        "property_plant_equipment": [

            "PropertyPlantAndEquipmentGross",
            "PropertyPlantAndEquipmentNet"

        ],

        "insurance_claim_reserves": [

            "LiabilityForUnpaidClaimsAndClaimsAdjustmentExpense",
            "LiabilityForUnpaidClaimsAndClaimsAdjustmentExpenseNet",
            "ShortdurationInsuranceContractsLiabilityForUnpaidClaimsAndAllocatedClaimAdjustmentExpenseNet",
            "LiabilityForClaimsAndClaimsAdjustmentExpense"

        ],

        "future_policy_benefit_reserves": [

            "LiabilityForFuturePolicyBenefits",
            "LiabilityForFuturePolicyBenefitsPeriodExpense"

        ],

        "unearned_premium_reserves": [

            "UnearnedPremiums",
            "ContractWithCustomerLiability",
            "DeferredRevenueCurrent"

        ],

        "deferred_tax_assets": [

            "DeferredTaxAssets",
            "DeferredTaxAssetsNet",
            "DeferredTaxAssetsLiabilitiesNet"

        ],

        "deferred_tax_liabilities": [

            "DeferredTaxLiabilities"

        ],

        "total_liabilities": [

            "Liabilities"

        ],

        "current_liabilities": [

            "LiabilitiesCurrent"

        ],

        "debt": [

            "DebtCurrent",
            "LongTermDebt",
            "LongTermDebtNoncurrent",
            "OtherLongTermDebt",
            "DebtInstrumentCarryingAmount",
            "DebtLongtermAndShorttermCombinedAmount",
            "SubordinatedDebt",
            "SeniorNotes",
            "ShortTermBorrowings",
            "LineOfCredit",
            "LineOfCreditFacilityAmountOutstanding",
            "LineOfCreditFacilityCurrentBorrowingCapacity",
            "LineOfCreditFacilityMaximumBorrowingCapacity",
            "LineOfCreditFacilityRemainingBorrowingCapacity",
            "DebtorInPossessionFinancingLettersOfCreditOutstanding"

        ],

        "lease_liabilities": [

            "OperatingLeaseLiability",
            "OperatingLeaseLiabilityCurrent",
            "OperatingLeaseLiabilityNoncurrent"

        ],

        "lease_assets": [

            "OperatingLeaseRightOfUseAsset"

        ],

        "stockholders_equity": [

            "StockholdersEquity",
            "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"

        ],

        "investments": [

            "Investments",
            "ShortTermInvestments"

        ],

        "insurance_liabilities": [

            "ReinsuranceRecoverableForUnpaidClaimsAndClaimsAdjustments"

        ],

        "marketable_securities": [

            "MarketableSecuritiesCurrent",
            "MarketableSecuritiesNoncurrent"

        ],

        "deferred_taxes": [

            "DeferredIncomeTaxesAndTaxCredits"

        ],

        "reinsurance_assets": [

            "ReinsuranceRecoverables",
            "ReinsuranceAssets"

        ],

        "tax_assets_and_liabilities": [

            "OperatingLossCarryforwards",
            "UnrecognizedTaxBenefits"

        ],

        "capital_assets": [

            "CapitalizedContractCostNet",
            "CapitalizedComputerSoftwareNet"

        ],

        "collateral_and_financing_assets": [

            "CollateralizedFinancings",
            "SecuritiesReceivedAsCollateral",
            "SecuritiesHeldAsCollateralAtFairValue",
            "SecuritiesLoanedFairValueOfCollateral"

        ],

        "equity": [

            "MinorityInterest",
            "NoncontrollingInterest",
            "PreferredStockValue",
            "CommonStockValue",
            "TreasuryStockValue",
            "RetainedEarningsAccumulatedDeficit",
            "AdditionalPaidInCapitalCommonStock",
            "MinimumNetCapitalRequired",
            "MinimumNetCapitalRequired1",
            "PreferredStockSharesIssued",
            "TreasuryStockCommonShares",

        ],

        "property_equipment_detail": [

            "BuildingsAndImprovementsGross",
            "MachineryAndEquipmentGross",
            "Land",
            "CapitalizedComputerSoftwareGross"

        ],

        "accumulated_depreciation": [

            "CapitalizedComputerSoftwareAmortization",
            "AdjustmentForAmortization",
            "CapitalizedComputerSoftwareAmortization1",
            "AmortizationOfDeferredCharges"

        ],

        "fair_value_assets_liabilities": [

            "AssetsFairValueDisclosure",
            "DebtInstrumentFairValue",
            "InterestRateFairValueHedgeAssetAtFairValue",
            "InterestRateFairValueHedgeLiabilityAtFairValue"

        ],

        "purchase_obligations": [

            "RecordedUnconditionalPurchaseObligationDueWithinOneYear",
            "RecordedUnconditionalPurchaseObligationDueInSecondYear",
            "RecordedUnconditionalPurchaseObligationDueInThirdYear",
            "RecordedUnconditionalPurchaseObligationDueInFourthYear",
            "UnrecordedUnconditionalPurchaseObligationBalanceOnFirstAnniversary",
            "UnrecordedUnconditionalPurchaseObligationBalanceOnSecondAnniversary",
            "UnrecordedUnconditionalPurchaseObligationBalanceOnThirdAnniversary",
            "UnrecordedUnconditionalPurchaseObligationBalanceOnFourthAnniversary",
            "UnrecordedUnconditionalPurchaseObligationBalanceOnFifthAnniversary",
            "UnrecordedUnconditionalPurchaseObligationDueAfterFiveYears"

        ],

        "valuation_allowances": [

            "ValuationAllowanceAmount"

        ],

        "restructuring_reserves": [

            "RestructuringReserveCurrent"

        ]

    },



# CASH FLOW STATEMENT

    "cash_flow": {

    "operating_cash_flow": [

        "NetCashProvidedByUsedInOperatingActivities"

    ],


    "investing_cash_flow": [

        "NetCashProvidedByUsedInInvestingActivities"

    ],


    "financing_cash_flow": [

        "NetCashProvidedByUsedInFinancingActivities"

    ],


    "capital_expenditures": [

        "PaymentsToAcquirePropertyPlantAndEquipment"

    ],


    "business_acquisitions": [

        "PaymentsToAcquireBusinessesNetOfCashAcquired",
        "BusinessAcquisitionCostOfAcquiredEntityCashPaid"

    ],


    "investment_purchases": [

        "PaymentsToAcquireAvailableForSaleSecurities",
        "PaymentsToAcquireAvailableForSaleSecuritiesDebt",
        "PaymentsToAcquireMarketableSecurities"

    ],


    "investment_sales": [

        "ProceedsFromSaleOfAvailableForSaleSecurities",
        "ProceedsFromSaleOfAvailableForSaleSecuritiesDebt"

    ],


    "property_sales": [

        "ProceedsFromSaleOfPropertyPlantAndEquipment"

    ],


    "dividends_paid": [

        "Dividends",
        "DividendsCommonStock",
        "DividendsCommonStockCash",
        "PaymentsOfDividends",
        "PaymentsOfDividendsCommonStock",
        "CashDividendsPaidToParentCompany"

    ],


    "debt_issued": [

        "ProceedsFromIssuanceOfLongTermDebt",
        "ProceedsFromIssuanceOfSeniorLongTermDebt",
        "ProceedsFromIssuanceOfUnsecuredDebt",
        "ProceedsFromNotesPayable",
        "ProceedsFromShortTermDebt",
        "ProceedsFromIssuanceOfCommercialPaper",
        "ProceedsFromLongTermLinesOfCredit"

    ],


    "debt_repayment": [

        "RepaymentsOfLongTermDebt",
        "RepaymentsOfNotesPayable",
        "RepaymentsOfSeniorDebt",
        "RepaymentsOfUnsecuredDebt",
        "RepaymentsOfShortTermDebt",
        "RepaymentsOfCommercialPaper",
        "RepaymentsOfLongTermLinesOfCredit"

    ],


    "stock_activity": [

        "TreasuryStockValueAcquiredCostMethod",
        "TreasuryStockAcquiredAverageCostPerShare",
        "PaymentsForRepurchaseOfCommonStock",
        "ProceedsFromStockOptionsExercised",
        "ProceedsFromContributionsFromParent"

    ],


    "cash_change": [

        "CashAndCashEquivalentsPeriodIncreaseDecrease"

    ],


    "tax_paid": [

        "IncomeTaxesPaidNet",
        "IncomeTaxPaidFederalAfterRefundReceived",
        "IncomeTaxPaidForeignAfterRefundReceived",
        "IncomeTaxPaidStateAndLocalAfterRefundReceived",
        "ProceedsFromIncomeTaxRefunds"

    ],


    "working_capital_changes": [

        "IncreaseDecreaseInReceivables",
        "IncreaseDecreaseInDeferredRevenue",
        "IncreaseDecreaseInDeferredIncomeTaxes",
        "IncreaseDecreaseInOtherDeposits",
        "IncreaseDecreaseInOtherOperatingCapitalNet",
        "IncreaseDecreaseInBookOverdrafts",
        "IncreaseDecreaseInSecuritiesLendingPayable"

    ],


    "other_operating_cash_flow": [

        "OtherOperatingActivitiesCashFlowStatement",
        "PaymentsForLegalSettlements"

    ],


    "investment_activity": [

        "MarketableSecuritiesRealizedGainLossOtherThanTemporaryImpairmentsAmount",
        "PaymentsForProceedsFromOtherInvestingActivities",
        "PaymentsForProceedsFromHedgeFinancingActivities"

    ],


    "business_transactions": [

        "ProceedsFromDivestitureOfBusinesses",
        "ProceedsFromDivestitureOfBusinessesNetOfCashDivested",
        "CashDivestedFromDeconsolidation",
        "DisposalGroupIncludingDiscontinuedOperationCashAndCashEquivalents"

    ],


    "other_financing_activity": [

        "ProceedsFromPaymentsForOtherFinancingActivities",
        "ProceedsFromRepaymentsOfBankOverdrafts"

    ],


    "restricted_cash_changes": [

        "IncreaseDecreaseInCollateralHeldUnderSecuritiesLending"

    ],


    "lease_payments": [

        "OperatingLeasePayments"

    ],


    "debt_activity": [

        "PaymentsOfDebtIssuanceCosts"

    ],


    "interest_paid": [

        "InterestPaid",
        "InterestPaidNet"

    ]

}
}






