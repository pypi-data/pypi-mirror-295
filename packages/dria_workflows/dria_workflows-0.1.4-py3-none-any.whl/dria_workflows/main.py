import logging

from dria_workflows import WorkflowBuilder, ConditionBuilder, Operator, Write, Edge, Read, Peek, Expression


def generate_random_vars(
        input_data: dict,
        max_time: int = 300,
        max_steps: int = 30,
        max_tokens: int = 750,
):
    """ Generate random variables for simulation

    Args:
        input_data (dict): External memory
        max_time (int, optional): Maximum time to run the workflow. Defaults to 300.
        max_steps (int, optional): Maximum number of steps to run the workflow. Defaults to 30.
        max_tokens (int, optional): Maximum number of tokens to run the workflow. Defaults to 750.

    Returns:
        dict: The generated random variables.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    builder = WorkflowBuilder(memory=input_data)
    builder.set_max_time(max_time)
    builder.set_max_steps(max_steps)
    builder.set_max_tokens(max_tokens)

    # TODO: prompts as md file
    # Step A: RandomVarGen
    builder.generative_step(
        id="random_var_gen",
        path="p1.md",
        operator=Operator.GENERATION,
        inputs=[
            Peek.new(index=0, key="simulation_description", required=True),
            Read.new(key="is_valid", required=False)
        ],
        outputs=[Write.new("random_vars")]
    )

    # Step B: ValidateRandomVars
    builder.generative_step(
        id="validate_random_vars",
        path="p2.md",
        operator=Operator.GENERATION,
        inputs=[Peek.new(index=0, key="simulation_description", required=True)],
        outputs=[Write.new("is_valid")]
    )

    flow = [
        Edge(source="random_var_gen", target="validate_random_vars"),
        Edge(source="validate_random_vars", target="_end",
             condition=ConditionBuilder.build(input=Read.new("random_vars", required=True), expression=Expression.EQUAL,
                                              expected="Yes", target_if_not="A"))
    ]
    builder.flow(flow)

    builder.set_return_value("random_vars")
    workflow = builder.build()

    return workflow.model_dump_json(indent=2, exclude_unset=True, exclude_none=True)


def main():
    wf = generate_random_vars({"simulation_description": ["VCs who interested with AI, Crypto intersection"],"persona_traits": ["Helpful, kind and educational"]})
    print("")


if __name__ == "__main__":
    main()