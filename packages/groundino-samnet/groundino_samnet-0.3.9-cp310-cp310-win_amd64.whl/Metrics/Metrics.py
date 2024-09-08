import torch
import numpy as np
import pandas as pd
from typing import Tuple
class Metrics():
  """
  Class for segmentation metrics
  """
  def __init__(self,smooth=1e-6):
    """
    Args:
      smooth: A float value added to the denominator for numerical stability.
    """
    self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    self.smooth = torch.tensor(smooth,dtype=torch.float32).to(device=self.device)


  def calculate_metrics(self,y_pred,y_true):
    """
    Calculate the metrics

    Args:
      y_true: True labels
      y_pred: Predicted labels

    Returns:
      A dictionary with the metrics
    """
    y_pred = y_pred.to(device=self.device)
    y_true = y_true.to(device=self.device)
    jaccard = self.jaccard(y_pred,y_true)
    dice = self.dice(y_pred,y_true)
    sensitivity = self.sensitivity(y_pred,y_true)
    specificity = self.specificity(y_pred,y_true)
    return {
        'jaccard':jaccard,
        'dice':dice,
        'sensitivity':sensitivity,
        'specificity':specificity,
    }
  """
  def __call__(self,y_true,y_pred):
    return self.calculate_metrics(y_true,y_pred)
  """
  def calculate_average_mask_metrics(data: dict) -> Tuple[pd.DataFrame,pd.DataFrame]:
    metricasc = []
    for i in range(len(data['Images'])):
      metricas = Metrics().calculate_metrics(data['Original'][i],data['Prediction'][i])
      metricasc.append(metricas)
      
        # Asegúrate de que la lista no esté vacía
    if not metricasc:
        return {}
    df_metrics = pd.DataFrame(metricasc)
    df_metrics.insert(0,"id",data['ids'])
    # Extrae las claves de los diccionarios
    keys = metricasc[0].keys()

    # Convierte la lista de diccionarios en un array de numpy
    array = np.array([[d[key] for key in keys] for d in metricasc])

    # Calcula el promedio a lo largo del eje 0
    avg_array = np.mean(array, axis=0)

    # Convierte el array promedio de vuelta a un diccionario
    avg_dict = {key: avg_array[i] for i, key in enumerate(keys)}
    # Imprime cada clave con su valor promedio
    for key, value in avg_dict.items():
        print(f"{key} Promedio = {value}")
    
    df_prom = pd.DataFrame([avg_dict])
    return df_metrics, df_prom
  
  def calculate_confusion_matrix(self,y_true,y_pred):
    """
    Calculate the confusion matrix

    Args:
      y_true: True labels
      y_pred: Predicted labels

    Returns:
      tp: True positives
      fp: False positives
      fn: False negatives
      tn: True negatives
    """
    output = torch.flatten(y_pred).to(torch.bool)
    target = torch.flatten(y_true).to(torch.bool)
    tp = torch.count_nonzero(output & target).to(torch.float32) # TP
    fp = torch.count_nonzero(output & ~target).to(torch.float32)  # FP
    fn = torch.count_nonzero(~output & target).to(torch.float32)  # FN
    tn = torch.count_nonzero(~output & ~target).to(torch.float32)  # TN
    return tp,fp,fn,tn

  def jaccard(self,y_pred,y_true):
    """
    Calculate the Jaccard or IoU score

    Args:
      y_pred: Predicted labels
      y_true: True labels

    Returns:
      The Jaccard or IoU score
    """
    tp,fp,fn,tn = self.calculate_confusion_matrix(y_pred=y_pred,y_true=y_true)
    return (tp / (tp + fp + fn + self.smooth)).cpu().detach().item()


  def dice(self,y_pred,y_true):
    """
    Calculate the Dice score

    Args:
      y_pred: Predicted labels
      y_true: True labels

    Returns:
      The Dice score
    """
    tp,fp,fn,tn = self.calculate_confusion_matrix(y_pred=y_pred,y_true=y_true)
    return (2 * tp / (2 * tp + fp + fn + self.smooth)).cpu().detach().item()


  def mIoU(self,y_pred,y_true):
    """
    Calculate the mIoU score

    Args:
      y_pred: Predicted labels
      y_true: True labels

    Returns:
      The mIoU score
    """
    tp,fp,fn,tn = self.calculate_confusion_matrix(y_pred=y_pred,y_true=y_true)
    iou_background = tn / (tn + fp + fn + self.smooth)
    iou_object = tp / (tp + fp + fn + self.smooth)
    return ((iou_background + iou_object) / 2.0).cpu().detach().item()


  def sensitivity(self,y_pred,y_true):
    """
    Calculate the sensitivity score

    Args:
      y_pred: Predicted labels
      y_true: True labels

    Returns:
      The sensitivity score
    """
    tp,fp,fn,tn = self.calculate_confusion_matrix(y_pred=y_pred,y_true=y_true)
    return (tp / (tp + fn + self.smooth)).cpu().detach().item()


  def specificity(self,y_pred, y_true):
    """
    Calculate the specificity score

    Args:
      y_pred: Predicted labels
      y_true: True labels

    Returns:
      The specificity score
    """
    tp,fp,fn,tn = self.calculate_confusion_matrix(y_pred=y_pred,y_true=y_true)
    return (tn / (tn + fp + self.smooth)).cpu().detach().item()

  def get_device(self):
    """
    Get the device used by the model.

    Returns:
      The device used by the metrics.
    """
    print(f"Device: {self.device}")
    return self.device