# LendingpoolBorrowEvent

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Identifier for the borrow event. | 
**reserve** | **str** | Ethereum address of the reserve from which the amount was borrowed. | 
**user** | **str** | Ethereum address of the user who borrowed. | 
**on_behalf_of** | **str** | Ethereum address of the entity on whose behalf the borrowing occurred. | [optional] 
**amount** | **str** | The borrowed amount. | 
**borrow_rate_mode** | **str** | The mode of borrowing rate (e.g., stable, variable). | 
**borrow_rate** | **str** | The interest rate for the borrowed amount. | 
**referral** | **int** | Referral code or identifier. | [optional] 
**raw** | [**Log**](Log.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


