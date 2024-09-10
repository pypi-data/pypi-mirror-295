# LendingpoolLiquidationCallEvent

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Identifier for the liquidation call event. | 
**collateral_asset** | **str** | Ethereum address of the collateral asset involved in the liquidation call. | 
**debt_asset** | **str** | Ethereum address of the debt asset involved in the liquidation call. | 
**user** | **str** | Ethereum address of the user being liquidated. | 
**debt_to_cover** | **str** | The amount of debt to cover during the liquidation. | 
**liquidated_collateral_amount** | **str** | The amount of collateral that was liquidated. | 
**liquidator** | **str** | Ethereum address of the liquidator who initiated the liquidation. | 
**receive_z_token** | **bool** | Indicates if the liquidator chose to receive ZTokens. | 
**raw** | [**Log**](Log.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


