using UnityEngine;
using System.Collections;



public class Main : MonoBehaviour {

	public TextAsset jsonFile;
	public Texture2D sourceTex;
	public Texture2D destTex;
	public Texture2D transTex;
	


	// Use this for initialization
	void Start () 
	{
		
		JSONObject json = new JSONObject(jsonFile.text);	
		
		foreach (JSONObject psdlayer in json.list)
		{
			//TODO just pass JSON object and extra fields in CopyPixels
			CopyPixels(sourceTex.width,sourceTex.height,(int)psdlayer["atlasx"].i,(int)psdlayer["atlasy"].i,(int)psdlayer["width"].i,(int)psdlayer["height"].i,(int)psdlayer["x"].i,(int)psdlayer["y"].i,(int)psdlayer["psdwidth"].i,(int)psdlayer["psdheight"].i,(int)psdlayer["z_order"].i);
		}
	
					
	}
	
	
	private void CopyPixels(int atlasWidth,int atlasHeight, int atlasX, int atlasY,int width,int height,int x,int y,int psdwidth, int psdheight, int z_order)
	{		
		Color[] clearpix = transTex.GetPixels(0,0,psdwidth,psdheight);
		Color[] pix = sourceTex.GetPixels(atlasX,(atlasHeight-atlasY-height),width,height);
		Texture2D destTex = new Texture2D(psdwidth, psdheight);
		//TODO create bbox sprites and move x,y instead of drawing layer with identical sizes
		destTex.SetPixels(0,0,psdwidth,psdheight,clearpix);
		destTex.Apply();
		
		destTex.SetPixels(x,psdheight - y - height,width,height,pix);
		destTex.Apply();
		
		GameObject go = new GameObject("psd - layer " + z_order);
		go.AddComponent<SpriteRenderer>();
		go.GetComponent<SpriteRenderer>().sprite =  Sprite.Create(destTex,new Rect(0,0,destTex.width,destTex.height),new Vector2(0,0));		
		go.GetComponent<SpriteRenderer>().sortingOrder = 100 - z_order ;
	}
	
	
}
