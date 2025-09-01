#!/usr/bin/env python3
"""
Speech-to-Text converter using Vosk library

This script can be used standalone or imported as a module.
Requires vosk-model-en-us-0.22-lgraph folder in the same directory.

Usage:
    Standalone: python speech_to_text.py audio_file.wav
    Import: from speech_to_text import transcribe_audio
"""

import json
import os
import sys
import wave
import argparse
from typing import Optional, Dict, Any

try:
    import vosk
except ImportError:
    print("Error: vosk library not installed. Install with: pip install vosk")
    sys.exit(1)


def transcribe_audio(
    audio_file_path: str, 
    model_path: str = "vosk-model-en-us-0.22-lgraph",
    return_detailed: bool = False
) -> Optional[str | Dict[Any, Any]]:
    """
    Transcribe audio file to text using Vosk speech recognition.
    
    Args:
        audio_file_path (str): Path to the WAV audio file
        model_path (str): Path to Vosk model directory (default: vosk-model-en-us-0.22-lgraph)
        return_detailed (bool): If True, return full JSON response; if False, return only text
        
    Returns:
        str | Dict | None: Transcribed text or detailed JSON response, None if error
        
    Raises:
        FileNotFoundError: If audio file or model directory not found
        ValueError: If audio file format is not supported
    """
    
    # Check if audio file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    # Get absolute path for model directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_model_path = os.path.join(script_dir, model_path)
    
    # Check if model directory exists
    if not os.path.exists(full_model_path):
        raise FileNotFoundError(f"Vosk model not found: {full_model_path}")
    
    try:
        # Initialize Vosk model
        vosk.SetLogLevel(-1)  # Suppress Vosk logs
        model = vosk.Model(full_model_path)
        
        # Open and validate WAV file
        with wave.open(audio_file_path, 'rb') as wf:
            # Check audio format
            if wf.getnchannels() != 1:
                raise ValueError("Audio must be mono (1 channel)")
            if wf.getsampwidth() != 2:
                raise ValueError("Audio must be 16-bit")
            if wf.getcomptype() != 'NONE':
                raise ValueError("Audio must be uncompressed WAV")
                
            sample_rate = wf.getframerate()
            
            # Create recognizer
            rec = vosk.KaldiRecognizer(model, sample_rate)
            rec.SetWords(True)  # Enable word-level timestamps
            
            results = []
            
            # Process audio in chunks
            chunk_size = 4000
            while True:
                data = wf.readframes(chunk_size)
                if len(data) == 0:
                    break
                    
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get('text', '').strip():
                        results.append(result)
            
            # Get final result
            final_result = json.loads(rec.FinalResult())
            if final_result.get('text', '').strip():
                results.append(final_result)
            
            # Combine all results
            if not results:
                return "" if not return_detailed else {"text": "", "words": []}
            
            # Combine text from all results
            full_text = " ".join(result.get('text', '') for result in results if result.get('text', '').strip())
            print(full_text)
            
            if return_detailed:
                # Combine all word-level information
                all_words = []
                for result in results:
                    if 'result' in result:
                        all_words.extend(result['result'])
                
                return {
                    "text": full_text,
                    "words": all_words,
                    "confidence": sum(word.get('conf', 0) for word in all_words) / len(all_words) if all_words else 0
                }
            else:
                return full_text
                
    except wave.Error as e:
        raise ValueError(f"Invalid WAV file format: {e}")
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


def main():
    """Main function for standalone usage"""
    parser = argparse.ArgumentParser(description="Convert speech to text using Vosk")
    parser.add_argument("audio_file", help="Path to WAV audio file")
    parser.add_argument("--model", "-m", default="vosk-model-en-us-0.22-lgraph", 
                       help="Path to Vosk model directory (default: vosk-model-en-us-0.22-lgraph)")
    parser.add_argument("--detailed", "-d", action="store_true", 
                       help="Return detailed JSON output with word-level info")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    
    args = parser.parse_args()
    
    try:
        print(f"Transcribing: {args.audio_file}")
        print("Processing... Please wait.")
        
        result = transcribe_audio(args.audio_file, args.model, args.detailed)
        
        if result is None:
            print("Transcription failed!")
            sys.exit(1)
        
        if args.detailed:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = result
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Result saved to: {args.output}")
        else:
            print("\n" + "="*50)
            print("TRANSCRIPTION RESULT:")
            print("="*50)
            print(output)
            print("="*50)
            
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nTranscription cancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
