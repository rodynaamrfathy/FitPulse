document.querySelectorAll('.start-button').forEach(button => {
    button.addEventListener('click', () => {
        const time = parseInt(button.getAttribute('data-time'), 10);
        const sets = parseInt(button.getAttribute('data-sets'), 10);
        
        startTimer(time, sets);
    });
});

function startTimer(time, sets) {
    const progressContainer = document.getElementById('progress-container');
    const setMessage = document.getElementById('set-message');
    const finishedButton = document.getElementById('finished-button');
    const rewardMessage = document.getElementById('reward-message');

    progressContainer.innerHTML = '';
    
    const timerContainer = document.getElementById('timer-container');
    timerContainer.classList.remove('hidden');

    let currentSet = 1;

    function runSet() {
        
        const progressBar = document.createElement('div');
        progressBar.classList.add('progress-bar');
        progressBar.style.width = '100%'; 
        progressContainer.appendChild(progressBar);

        let currentTime = time; 

        const interval = setInterval(() => {
            currentTime--;

            const percent = (currentTime / time) * 100;
            progressBar.style.width = percent + '%';

            setMessage.textContent = `Set ${currentSet} remaining: ${currentTime} seconds left`;

            if (currentTime <= 0) {
                clearInterval(interval); 
                setMessage.textContent = `Set ${currentSet} complete!`; 
                
                currentSet++;
                
                if (currentSet <= sets) {
                    runSet(); 
                } else {
                    setMessage.textContent = "Workout Complete!"; 
                    finishedButton.classList.remove('hidden');
                    rewardMessage.classList.remove('hidden'); 
                }
            }
        }, 1000);
    }

    runSet(); 
}
