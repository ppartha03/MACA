from TextData import TextData
from MturkData import MturkData


from preprocessing import AbstractPreprocessor
from postprocessing import AbstractPostprocessor
from agents import AbstractAgent

class MturkScoringPreprocessingAdapter(AbstractPreprocessor.AbstractPreprocessor):
    def __init__(self, preprocessing_class, *args, **kwargs):
        self.preprocessing = preprocessing_class(*args, **kwargs)

    def preprocess(self, data):
        """
            We expect an object of type MturkData here.
        """
        content = data.data

        response = self.preprocessing.preprocess(TextData(content))
        data.data = response
        # Alternatively we may opt to create new object.
        # return MturkData.create_object_from(data, response)
        return data

class MturkScoringPostProcessing(AbstractPostprocessor.AbstractPostprocessor):
    def __init__(self, postprocessing_class, *args, **kwargs):
        self.postprocessing = postprocessing_class(*args, **kwargs)

    def postprocess(self, data):
        """
            We expect an object of type MturkData here.
        """
        content = data.data

        response = self.postprocessing.postprocess(content)
        data.data = response
        # Alternatively we may opt to create new object.
        # return MturkData.create_object_from(data, response)
        return data

class MturkScoringAgentAdapter(AbstractAgent.AbstractAgent):
    def __init__(self, agent_class, *args, **kwargs):
        super(MturkScoringAgentAdapter, self).__init__()
        self.agent = agent_class(*args, **kwargs)

    def process_inputs(self, inputs):
        pass

    def full_process(self, inputs):
        """
            Received from preprocessing units.
        """

        reference_objects = [data[0] for data in inputs]
        extracted_data = [[data[0].data] for data in inputs]

        self.agent.full_process(extracted_data)

        index = 0
        outputs = []

        while not self.agent.output_data.empty():
            output = self.agent.next_output(timeout = 0)
            assert output is not None
            reference_objects[index].data = output
            outputs.append(reference_objects[index])
            index += 1

        assert index == len(reference_objects)
        for output in outputs:
            self.queue_output(output)

        return None

    def model_postprocess(self, outputs):
        return None # No need to do anything here since everything is handled in full process