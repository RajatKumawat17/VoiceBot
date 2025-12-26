# How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Ensure `.env` has:
   ```
   LIVEKIT_URL=...
   LIVEKIT_API_KEY=...
   LIVEKIT_API_SECRET=...
   OPENAI_API_KEY=...
   DEEPGRAM_API_KEY=...
   ```

3. **Run the Agent**:
   ```bash
   python agent.py dev
   ```

4. **Dynamic Updates**:
   - Edit `system_prompt.txt` to change the persona on the fly.
   - Edit `knowledge_base.txt` to update what the agent knows.