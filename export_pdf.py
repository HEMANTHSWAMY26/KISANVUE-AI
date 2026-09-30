import os
import sys

def pptx_to_pdf(input_pptx, output_pdf):
    abs_input = os.path.abspath(input_pptx)
    abs_output = os.path.abspath(output_pdf)
    print(f"Converting {abs_input} to {abs_output} using PowerPoint COM...")
    
    import comtypes.client
    import comtypes
    
    # Initialize PowerPoint
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    # ppFixedFormatTypePDF = 2
    try:
        deck = powerpoint.Presentations.Open(abs_input, WithWindow=False)
        deck.SaveAs(abs_output, 32) # 32 is ppSaveAsPDF
        deck.Close()
        print(f"Successfully exported PDF: {abs_output}")
    except Exception as e:
        print(f"COM conversion error: {e}")
        raise
    finally:
        powerpoint.Quit()

if __name__ == "__main__":
    pptx_to_pdf("KISANVUE_AI_TRACK4_PITCH_DECK.pptx", "KISANVUE_AI_TRACK4_PITCH_DECK.pdf")
