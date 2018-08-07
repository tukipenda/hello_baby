tutorial_message=[
    'First turn the warmer on.',
    "These are the tabs you can use when you set up the warmer.  Remember that BIG RED BUTTON.  That's how you deliver the baby",
    'You can adjust warmer settings here.  You can come back to the warmer tab to make more adjustments when the baby is delivered.',
    "Now you can fetch supplies.",
    "Time to deliver the baby.  Click the BIG RED BUTTON!",
    "Okay, you just clicked that big red button, and now the baby has been delivered.  Here's what you do next!",
    "These are the tabs you can use when the baby is delivered. You can also go back and review the history again if you need to with the history tab.",
    "Here is the tab where you check exams.",
    "This is the tab where you can pick actions to help the baby out.",
    "Here's how you start PPV",
    "You can adjust the settings for PPV before you get started",
    "Yay, you finished the tutorial!  Click below to start the simulation!"
]

var tutorial = new Vue({
    el: '#TutorialApp',
    delimiters: ['[[',']]'],
    data: {
      index:1,
        tutorial_message:tutorial_message
    }
});