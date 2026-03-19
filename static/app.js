/**
 * 汉诺塔可视化 - 超级玛丽主题
 * 核心JavaScript逻辑
 */

const state = {
    diskCount: 3,
    speed: 'medium',
    mode: 'auto',
    towers: { A: [], B: [], C: [] },
    steps: [],
    currentStep: 0,
    isPlaying: false,
    isPaused: false,
    timer: 0,
    timerInterval: null,
    selectedDisk: null,
    selectedTower: null,
    soundEnabled: true
};

class SoundSystem {
    constructor() {
        this.audioContext = null;
        this.initialized = false;
    }
    init() {
        if (this.initialized) return;
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.initialized = true;
        } catch (e) { console.warn('Web Audio API not supported'); }
    }
    playTone(frequency, duration, type = 'sine', volume = 0.3) {
        if (!state.soundEnabled || !this.audioContext) return;
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        oscillator.frequency.value = frequency;
        oscillator.type = type;
        gainNode.gain.setValueAtTime(volume, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
    playMove() { this.init(); this.playTone(523, 0.1, 'square', 0.2); setTimeout(() => this.playTone(659, 0.1, 'square', 0.2), 50); setTimeout(() => this.playTone(784, 0.15, 'square', 0.2), 100); }
    playWin() { this.init(); const notes = [523, 659, 784, 1047, 784, 1047]; const durations = [0.15, 0.15, 0.15, 0.3, 0.15, 0.4]; let time = 0; notes.forEach((note, i) => { setTimeout(() => this.playTone(note, durations[i], 'square', 0.25), time); time += durations[i] * 500; }); }
    playError() { this.init(); this.playTone(200, 0.2, 'sawtooth', 0.15); setTimeout(() => this.playTone(150, 0.3, 'sawtooth', 0.15), 100); }
}

const soundSystem = new SoundSystem();
const SPEED_CONFIG = { slow: 1500, medium: 800, fast: 300 };

document.addEventListener('DOMContentLoaded', () => { initializeGame(); setupEventListeners(); });

function initializeGame() {
    state.towers = { A: [], B: [], C: [] };
    state.steps = [];
    state.currentStep = 0;
    state.isPlaying = false;
    state.isPaused = false;
    state.timer = 0;
    state.selectedDisk = null;
    state.selectedTower = null;
    if (state.timerInterval) { clearInterval(state.timerInterval); state.timerInterval = null; }
    for (let i = state.diskCount; i >= 1; i--) { state.towers.A.push(i); }
    generateSteps(state.diskCount, 'A', 'C', 'B');
    renderTowers(); renderStepsList(); updateStats(); updateTimer();
    document.getElementById('celebration').classList.remove('show');
}

function setupEventListeners() {
    const diskCountInput = document.getElementById('disk-count');
    diskCountInput.addEventListener('change', (e) => {
        let value = parseInt(e.target.value);
        if (isNaN(value) || value < 1) value = 1;
        if (value > 10) value = 10;
        e.target.value = value;
        state.diskCount = value;
        reset();
    });
    document.querySelectorAll('.tower').forEach(tower => {
        tower.addEventListener('click', (e) => { if (state.mode === 'manual') handleTowerClick(tower.dataset.tower); });
    });
}

function generateSteps(n, from, to, aux) {
    if (n === 0) return;
    generateSteps(n - 1, from, aux, to);
    state.steps.push({ disk: n, from: from, to: to, description: `移动圆盘 ${n} 从 ${from} 到 ${to}` });
    generateSteps(n - 1, aux, to, from);
}

function renderTowers() {
    ['A', 'B', 'C'].forEach(towerId => {
        const container = document.querySelector(`#tower-${towerId} .disks-container`);
        container.innerHTML = '';
        state.towers[towerId].forEach((diskSize, index) => {
            const disk = document.createElement('div');
            disk.className = `disk disk-${diskSize}`;
            disk.dataset.size = diskSize;
            if (index === state.towers[towerId].length - 1 && state.mode === 'manual') disk.style.cursor = 'pointer';
            container.appendChild(disk);
        });
    });
}

function renderStepsList() {
    const stepsList = document.getElementById('steps-list');
    stepsList.innerHTML = '';
    state.steps.forEach((step, index) => {
        const li = document.createElement('li');
        li.textContent = step.description;
        if (index < state.currentStep) li.classList.add('completed');
        else if (index === state.currentStep) li.classList.add('current');
        stepsList.appendChild(li);
    });
}

function updateStats() { document.getElementById('step-count').textContent = `${state.currentStep} / ${state.steps.length}`; }
function updateTimer() { const m = Math.floor(state.timer / 60), s = state.timer % 60; document.getElementById('timer').textContent = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`; }
function changeDiskCount(delta) { const input = document.getElementById('disk-count'); let value = parseInt(input.value) + delta; if (value < 1) value = 1; if (value > 10) value = 10; input.value = value; state.diskCount = value; reset(); }
function setSpeed(speed) { state.speed = speed; document.querySelectorAll('.speed-btn').forEach(btn => { btn.classList.toggle('active', btn.dataset.speed === speed); }); }
function setMode(mode) { state.mode = mode; document.querySelectorAll('.mode-btn').forEach(btn => { btn.classList.toggle('active', btn.dataset.mode === mode); }); reset(); }
function play() { if (state.mode === 'manual' || state.currentStep >= state.steps.length || (state.isPlaying && !state.isPaused)) return; state.isPlaying = true; state.isPaused = false; if (!state.timerInterval) state.timerInterval = setInterval(() => { state.timer++; updateTimer(); }, 1000); autoPlay(); }
function pause() { state.isPaused = true; state.isPlaying = false; if (state.timerInterval) { clearInterval(state.timerInterval); state.timerInterval = null; } }
function prevStep() { if (state.currentStep <= 0) return; pause(); state.currentStep--; const step = state.steps[state.currentStep]; state.towers[step.to].pop(); state.towers[step.from].push(step.disk); renderTowers(); renderStepsList(); updateStats(); }
function nextStep() { if (state.currentStep >= state.steps.length) return; pause(); executeStep(state.currentStep); state.currentStep++; renderTowers(); renderStepsList(); updateStats(); checkCompletion(); }
function reset() { pause(); state.diskCount = parseInt(document.getElementById('disk-count').value) || 3; initializeGame(); }
async function autoPlay() { while (state.isPlaying && !state.isPaused && state.currentStep < state.steps.length) { await executeStepWithAnimation(state.currentStep); if (!state.isPlaying || state.isPaused) break; state.currentStep++; renderStepsList(); updateStats(); if (state.currentStep >= state.steps.length) { checkCompletion(); break; } await sleep(SPEED_CONFIG[state.speed]); } }
function executeStep(stepIndex) { const step = state.steps[stepIndex]; state.towers[step.from].pop(); state.towers[step.to].push(step.disk); }
async function executeStepWithAnimation(stepIndex) { const step = state.steps[stepIndex]; const fromContainer = document.querySelector(`#tower-${step.from} .disks-container`); const toContainer = document.querySelector(`#tower-${step.to} .disks-container`); const diskElement = fromContainer.lastElementChild; if (!diskElement) { executeStep(stepIndex); return; } diskElement.classList.add('moving'); state.towers[step.from].pop(); state.towers[step.to].push(step.disk); await sleep(SPEED_CONFIG[state.speed] / 2); fromContainer.removeChild(diskElement); toContainer.appendChild(diskElement); diskElement.classList.remove('moving'); }
function handleTowerClick(towerId) { if (!state.isPlaying) { state.isPlaying = true; if (!state.timerInterval) state.timerInterval = setInterval(() => { state.timer++; updateTimer(); }, 1000); } const tower = state.towers[towerId]; if (state.selectedDisk === null) { if (tower.length === 0) return; state.selectedDisk = tower[tower.length - 1]; state.selectedTower = towerId; const diskElement = document.querySelector(`#tower-${towerId} .disks-container`).lastElementChild; if (diskElement) diskElement.classList.add('selected'); } else { if (towerId === state.selectedTower) { clearSelection(); return; } if (tower.length > 0 && tower[tower.length - 1] < state.selectedDisk) { clearSelection(); return; } moveDisk(state.selectedTower, towerId, state.selectedDisk); clearSelection(); checkCompletion(); } }
function moveDisk(from, to, disk) { state.towers[from].pop(); state.towers[to].push(disk); state.currentStep++; soundSystem.playMove(); renderTowers(); updateStats(); }
function clearSelection() { if (state.selectedTower) { const diskElement = document.querySelector(`#tower-${state.selectedTower} .disks-container .disk.selected`); if (diskElement) diskElement.classList.remove('selected'); } state.selectedDisk = null; state.selectedTower = null; }
function checkCompletion() { if (state.towers.C.length === state.diskCount) { pause(); showCelebration(); } }
function showCelebration() { const celebration = document.getElementById('celebration'); celebration.classList.add('show'); soundSystem.playWin(); const confettiContainer = document.getElementById('confetti'); confettiContainer.innerHTML = ''; const colors = ['#ff6b6b', '#ffa94d', '#ffd43b', '#69db7c', '#4dabf7', '#9775fa', '#f783ac']; for (let i = 0; i < 100; i++) { const confetti = document.createElement('div'); confetti.className = 'confetti'; confetti.style.left = `${Math.random() * 100}%`; confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)]; confetti.style.animationDelay = `${Math.random() * 2}s`; confetti.style.animationDuration = `${2 + Math.random() * 2}s`; confettiContainer.appendChild(confetti); } setTimeout(() => { celebration.classList.remove('show'); }, 5000); }
function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
function showError(message) { const toast = document.getElementById('error-toast'); toast.querySelector('.error-message').textContent = message; toast.classList.add('show'); setTimeout(() => { toast.classList.remove('show'); }, 3000); }
function toggleSound() { state.soundEnabled = !state.soundEnabled; const btn = document.getElementById('sound-toggle'); if (state.soundEnabled) { btn.textContent = '🔊 开'; btn.classList.remove('muted'); } else { btn.textContent = '🔇 关'; btn.classList.add('muted'); } }
window.changeDiskCount = changeDiskCount; window.setSpeed = setSpeed; window.setMode = setMode; window.play = play; window.pause = pause; window.prevStep = prevStep; window.nextStep = nextStep; window.reset = reset; window.toggleSound = toggleSound;