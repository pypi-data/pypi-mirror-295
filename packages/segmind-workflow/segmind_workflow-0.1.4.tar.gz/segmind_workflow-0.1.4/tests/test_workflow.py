# import unittest
# from unittest.mock import patch, MagicMock
# from segmind_workflow import Workflow

# class TestWorkflow(unittest.TestCase):
    
#     def setUp(self):
#         """
#         Setup test environment before each test.
#         """
#         self.api_key = "test_api_key"
#         self.workflow = Workflow(self.api_key)

#     @patch('requests.get')
#     def test_query(self, mock_get):
#         """
#         Test the query function to make sure it updates the function call sequence and context.
#         """
#         # Mock the response from the GET request
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             "function_call_sequence": ["function1", "function2"],
#             "new_context": "updated_context"
#         }
#         mock_get.return_value = mock_response

#         # Call the query method
#         prompt = "Test prompt"
#         self.workflow.query(prompt)

#         # Check if the context and call_sequence are updated
#         self.assertEqual(self.workflow.context, "updated_context")
#         self.assertEqual(self.workflow.call_sequence, ["function1", "function2"])
#         self.assertTrue(self.workflow.sequence_generated)

#     @patch('requests.post')
#     def test_call(self, mock_post):
#         """
#         Test the call function and ensure make_function_call is invoked for each function in the sequence.
#         """
#         # Set up the query first
#         self.workflow.call_sequence = ["function1", "function2"]
#         self.workflow.sequence_generated = True
        
#         # Mock the response for the POST request for make_function_call
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.json.side_effect = [
#             {"result": "result1", "credits_left": 90},
#             {"result": "result2", "credits_left": 80}
#         ]
#         mock_post.return_value = mock_response

#         # Call the call function
#         input_data = {"input": "test_data"}
#         self.workflow.call(input_data)

#         # Verify that the results and credits_left are updated
#         self.assertEqual(self.workflow.results, ["result1", "result2"])
#         self.assertEqual(self.workflow.credits_left, 80)
#         self.assertTrue(self.workflow.call_made)

#     def test_get_sequence(self):
#         """
#         Test that get_sequence raises an error if the sequence hasn't been generated.
#         """
#         with self.assertRaises(Exception) as context:
#             self.workflow.get_sequence()
        
#         self.assertTrue("Error: No query sequence generated yet. Please call query() first." in str(context.exception))
    
#     def test_get_result(self):
#         """
#         Test that get_result raises an error if no function call has been made.
#         """
#         with self.assertRaises(Exception) as context:
#             self.workflow.get_result()
        
#         self.assertTrue("Error: No function call made yet. Please call the functions first." in str(context.exception))

#     def test_w_of_cost(self):
#         """
#         Test the cost calculation function.
#         """
#         # Manually set the call sequence
#         self.workflow.call_sequence = ["function1", "function2"]
#         self.workflow.sequence_generated = True

#         # Calculate cost
#         total_cost = self.workflow.w_of_cost()

#         # Verify the total cost
#         self.assertEqual(total_cost, "Total cost: 30")  # 10 + 20 from the price list
    
#     def test_w_of_credits_left(self):
#         """
#         Test that get_credits_left raises an error if no function has been called.
#         """
#         with self.assertRaises(Exception) as context:
#             self.workflow.w_of_credits_left()
        
#         self.assertTrue("Error: No function call has been made. Credits not available." in str(context.exception))

#     def test_reset(self):
#         """
#         Test the reset function.
#         """
#         # Set some values
#         self.workflow.context = "test_context"
#         self.workflow.query_sequence = ["query1"]
#         self.workflow.call_sequence = ["function1"]
#         self.workflow.results = ["result1"]
#         self.workflow.sequence_generated = True
#         self.workflow.call_made = True
#         self.workflow.credits_left = 100
        
#         # Call the reset method
#         self.workflow.reset()
        
#         # Verify that everything except credits_left is reset
#         self.assertEqual(self.workflow.context, "")
#         self.assertEqual(self.workflow.query_sequence, [])
#         self.assertIsNone(self.workflow.call_sequence)
#         self.assertIsNone(self.workflow.results)
#         self.assertFalse(self.workflow.sequence_generated)
#         self.assertFalse(self.workflow.call_made)
#         self.assertEqual(self.workflow.credits_left, 100)

# if __name__ == "__main__":
#     unittest.main()

# # python -m unittest test_workflow.py