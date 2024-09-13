from fuxion.pipelines import DatasetPipeline

irp_chain = DatasetPipeline.from_template(
    generator_template="irp/generator.template",
    normalizer_template="irp/normalizer.template",
    few_shot_file="irp/irp.json",
    dataset_name=f"irp_dataset_test_z",
    k=2,
    model_name="gpt-4",
    cache=False,
    verbose=True,
    temperature=0.1,
)

result = irp_chain.execute()
print(result)
