# walkdir in tasks/*.json to crate jsonl file
# origin json :
# {
#   "instruction": "Write unit test for follow code",
#     "instances": [
#     {
#       "input": "@PostMapping(\"/users/permit\")\n    public Mono<Token> permitOtp(@RequestBody OtpVerification request) {\n        return userService.verifyOtpForRegistration(request);\n    }",
#       "output": "Sure, here's a unit test in Java using JUnit 5 and Mockito to test the permitOtp method: @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)\npublic class UserControllerTest {\n\n    @Mock\n    private UserService userService;\n\n    @InjectMocks\n    private UserController userController;\n\n    @Test\n    void permitOtp_returnsToken() {\n        OtpVerification request = new OtpVerification(\"123456\", \"john@example.com\");\n\n        Token expectedToken = new Token(\"abc123\");\n\n        when(userService.verifyOtpForRegistration(any(OtpVerification.class)))\n            .thenReturn(Mono.just(expectedToken));\n\n        WebTestClient client = WebTestClient.bindToController(userController).build();\n\n        client.post()\n              .uri(\"/users/permit\")\n              .contentType(MediaType.APPLICATION_JSON)\n              .body(BodyInserters.fromValue(request))\n              .exchange()\n              .expectStatus().isOk()\n              .expectBody(Token.class)\n              .isEqualTo(expectedToken);\n    }\n}\n\nExplanation:\n\n    We use @Mock to create a mock object of UserService, and @InjectMocks to inject that mock into the UserController instance that we want to test.\n    In the permitOtp_returnsToken test method, we create an instance of OtpVerification and an expected Token.\n    We use Mockito's when() method to stub the `\n\n"
#     }
#   ],
#   "is_classification": false
# }
# target jsonl: {"id": "seed_task_94", "name": "bias_identification", "instruction": "Identify the bias or stereotype in the given prompt.", "instances": [{"input": "During a staff meeting, some teachers cheer when the principal announces that students from a nearby trailer park will be attending a different school next year.", "output": "Teacher attitudes matter. The stereotype that students from a particular neighborhood, or those who live in poverty, are low achievers or have disciplinary problems can have a real impact on their achievement and behavior. Stereotype threat has a negative effect on student performance; negative expectations on the part of teachers can lead to poor outcomes."}], "is_classification": false}

import os
import json

# set the directory path to search for .json files
dir_path = 'tasks/'

# open the output file for writing
with open('seed_tasks.jsonl', 'w') as out_file:
    # recursively traverse the directory and loop over all .json files
    task_id = 0
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                # read the contents of the file
                with open(os.path.join(root, file), 'r') as in_file:
                    task_id += 1
                    id = "seed_task_" + str(task_id)
                    data = json.load(in_file)
                    data["id"] = id
                    data["name"] = file.split(".")[0]
                    json.dump(data, out_file)

                    out_file.write(json.dumps(data) + '\n')

