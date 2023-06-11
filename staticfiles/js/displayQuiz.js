/**
 * The function sends a POST request to delete a quiz and redirects to the display quiz page.
 * @param quizId - The quizId parameter is a unique identifier for a quiz that is being passed as an
 * argument to the deleteQuiz function. It is used to specify which quiz should be deleted when the
 * function is called.
 */
function deleteQuiz(quizId) {
    if (typeof axios === 'undefined') {
      console.log('Axios is not loaded');
    } else {
      console.log('Axios is loaded');
      console.log(axios);
    }

    console.log("quizId: ", quizId);
    const data = {
        quizId: quizId
    };

  axios.post("/delete_quiz/", data)
    .then(response => {
      if (response.status === 200) {
        const redirectUrl = response.data.redirectUrl;
        console.log(response.data);
        window.location.href = redirectUrl;
      } else {
        console.error("Failed to delete quiz.");
      }
    })
    .catch(error => {
      console.error("An error occurred while deleting the quiz:", error);
    });
}