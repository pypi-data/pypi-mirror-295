import hypersync
import asyncio


# Define events (matching the structure from the second code block)
event_1 = (
    "V3FundsDeposited(address inputToken,address outputToken,uint256 inputAmount,"
    "uint256 outputAmount,uint256 indexed destinationChainId,uint32 indexed depositId,"
    "uint32 quoteTimestamp,uint32 fillDeadline,uint32 exclusivityDeadline,"
    "address indexed depositor,address recipient,address exclusiveRelayer,bytes message)"
)
event_2 = (
    "RequestedSpeedUpV3Deposit(uint256 updatedOutputAmount,uint32 indexed depositId,"
    "address indexed depositor,address updatedRecipient,bytes updatedMessage,"
    "bytes depositorSignature)"
)
event_3 = (
    "FilledV3Relay(address inputToken,address outputToken,uint256 inputAmount,"
    "uint256 outputAmount,uint256 repaymentChainId,uint256 indexed originChainId,"
    "uint32 indexed depositId,uint32 fillDeadline,uint32 exclusivityDeadline,"
    "address exclusiveRelayer,address indexed relayer,address depositor,"
    "address recipient,bytes message,V3RelayExecutionEventInfo relayExecutionInfo)"
)
event_4 = (
    "RequestedV3SlowFill(address inputToken,address outputToken,uint256 inputAmount,"
    "uint256 outputAmount,uint256 indexed originChainId,uint32 indexed depositId,"
    "uint32 fillDeadline,uint32 exclusivityDeadline,address exclusiveRelayer,"
    "address depositor,address recipient,bytes message)"
)

# List of events
events_set = [event_1, event_2, event_3, event_4]

# Hypersync client configuration
hypersync_client_url = "https://base.hypersync.xyz"
contract = "0x09aea4b2242abC8bb4BB78D537A67a245A7bEC64"


async def main():
    # Create Hypersync client using the provided base URL
    client = hypersync.HypersyncClient(hypersync.ClientConfig(url=hypersync_client_url))

    # Lowercase the smart contract address
    smart_contract = contract.lower()

    # Iterate over the list of events
    for event in events_set:
        try:
            # Convert event signature to topic0 (hash of the event signature)
            topic = hypersync.signature_to_topic0(event)

            # Prepare the query to fetch logs for the event
            query = hypersync.preset_query_logs_of_event(
                smart_contract, topic, from_block=19_500_000
            )

            print("Running the query for event...")

            # Run the query and fetch the logs
            res = await client.get(query)

            # Check if logs were returned
            if len(res.data.logs) == 0:
                print("No logs found for event")
                continue

            # Process the logs (print the log count)
            print(f"Query returned {len(res.data.logs)} logs for event")

        except Exception as e:
            print(f"Error querying event, error: {e}")
            continue  # Continue to the next event


# Run the asynchronous main function
asyncio.run(main())
